"""The paper-scope-6-api dependencies module.

"""

from functools import lru_cache
from typing import Optional
from urllib.parse import urlparse

import httpx
import msal

from fastapi import Depends, Header, HTTPException, status
from jose import jwt
from pydantic import BaseSettings


class ElkSettings(BaseSettings):
    elastic_uri: str

    class Config:
        env_file = '.env.local'

    def __hash__(self):
        return hash(tuple(item for item in self.dict().items()))


@lru_cache
def get_elk_settings():
    return ElkSettings()


class AuthSettings(BaseSettings):
    b2c_client_id: str
    b2c_client_secret: str
    b2c_endpoint: str
    b2c_signupsignin_userflow: str
    elastic_authority: str
    elastic_client_id: str

    class Config:
        env_file = '.env.local'

    def __hash__(self):
        return hash(tuple(item for item in self.dict().items()))


@lru_cache
def get_auth_settings():
    return AuthSettings()


@lru_cache
def get_public_app(auth_settings: AuthSettings = Depends(get_auth_settings)):
    return msal.PublicClientApplication(
        auth_settings.b2c_client_id,
        authority=(
            f'{auth_settings.b2c_endpoint}/'
            f'{auth_settings.b2c_signupsignin_userflow}'
        ),
    )


@lru_cache
def get_private_app(auth_settings: AuthSettings = Depends(get_auth_settings)):
    return msal.ConfidentialClientApplication(
        auth_settings.b2c_client_id,
        client_credential=auth_settings.b2c_client_secret,
        authority=auth_settings.elastic_authority,
    )


async def get_current_user(
    auth_settings: AuthSettings = Depends(get_auth_settings),
    msal_app: msal.PublicClientApplication = Depends(get_public_app),
    authorization: Optional[str] = Header(None),
    x_ms_token_aad_id_token: Optional[str] = Header(None),
):
    tenant = urlparse(auth_settings.b2c_endpoint).path.lstrip('/')
    scopes = [
        f'https://{tenant}/{auth_settings.b2c_client_id}/user.impersonate',
    ]
    if payload := msal_app.acquire_token_silent(scopes, None):
        return f'{payload["given_name"]} {payload["family_name"]}'

    if authorization is None and x_ms_token_aad_id_token is None:
        detail = 'Authorization and X-MS-TOKEN-AAD-ID_TOKEN headers missing'
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'},
        )
    elif x_ms_token_aad_id_token is not None:
        token = x_ms_token_aad_id_token
    elif authorization.startswith('Bearer '):
        token = authorization.replace('Bearer ', '')
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header does not start with "Bearer "',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    try:
        jwks_uri = (
            f'{auth_settings.b2c_endpoint}/discovery/v2.0/keys?p='
            f'{auth_settings.b2c_signupsignin_userflow}'
        )
        header = jwt.get_unverified_header(token)
        async with httpx.AsyncClient() as client:
            resp = await client.get(jwks_uri)

        jwks = resp.json()
        key = [k for k in jwks['keys'] if k['kid'] == header['kid']].pop()
        payload = jwt.decode(
            token,
            key,
            algorithms=[header['alg']],
            audience=auth_settings.b2c_client_id,
        )
        if x_ms_token_aad_id_token is None and (
            'scp' not in payload or
            payload['scp'] != 'user.impersonate'
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Scope user.impersonate missing from access token',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return payload
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unable to find key with matching kid',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Error decoding access token',
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def get_obo_token(
    auth_settings: AuthSettings = Depends(get_auth_settings),
    msal_app: msal.ConfidentialClientApplication = Depends(get_private_app),
):
    tenant = urlparse(auth_settings.b2c_endpoint).path.lstrip('/')
    scopes = [
        f'https://{tenant}/{auth_settings.elastic_client_id}/.default',
    ]
    token_resp = msal_app.acquire_token_for_client(scopes)
    try:
        return token_resp['access_token']
    except KeyError:
        print(token_resp)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unable to acquire elastic access token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
