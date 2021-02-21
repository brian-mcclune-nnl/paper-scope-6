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


class AuthSettings(BaseSettings):
    b2c_client_id: str
    b2c_client_secret: str
    b2c_endpoint: str
    b2c_signupsignin_userflow: str

    class Config:
        env_file = '.env.local'

    def __hash__(self):
        return hash(tuple(item for item in self.dict().items()))


@lru_cache
def get_auth_settings():
    return AuthSettings()


@lru_cache
def get_msal_app(auth_settings: AuthSettings = Depends(get_auth_settings)):
    return msal.PublicClientApplication(
        auth_settings.b2c_client_id,
        authority=(
            f'{auth_settings.b2c_endpoint}/'
            f'{auth_settings.b2c_signupsignin_userflow}'
        ),
    )


async def get_current_user(
    auth_settings: AuthSettings = Depends(get_auth_settings),
    msal_app: msal.PublicClientApplication = Depends(get_msal_app),
    authorization: Optional[str] = Header(None),
):
    tenant = urlparse(auth_settings.b2c_endpoint).path.lstrip('/')
    scopes = [
        f'https://{tenant}/{auth_settings.b2c_client_id}/user.impersonate',
    ]
    if payload := msal_app.acquire_token_silent(scopes, None):
        return f'{payload["given_name"]} {payload["family_name"]}'

    if authorization is None or not authorization.startswith('Bearer '):
        detail = 'missing from headers' if authorization is None else \
            'does not start with Bearer'
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Authorization {detail}',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    try:
        jwks_uri = (
            f'{auth_settings.b2c_endpoint}/discovery/v2.0/keys?p='
            f'{auth_settings.b2c_signupsignin_userflow}'
        )
        token = authorization.replace('Bearer ', '')
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
        if 'scp' not in payload or payload['scp'] != 'user.impersonate':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Scope user.impersonate missing from access token',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return f'{payload["given_name"]} {payload["family_name"]}'
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Error decoding access token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
