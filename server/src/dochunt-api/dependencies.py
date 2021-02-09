"""The dochunt-api dependencies module.

"""

from functools import lru_cache
from typing import Optional

import httpx

from fastapi import Depends, Header, HTTPException, status
from jose import jwt
from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    jwks_uri: str = (
        'https://clunacy.b2clogin.com/clunacy.onmicrosoft.com/'
        'discovery/v2.0/keys?p=b2c_1_dochunt_signupsignin'
    )
    b2c_client_id: str
    b2c_client_secret: str

    class Config:
        env_file = '.env'


@lru_cache
def get_auth_settings():
    return AuthSettings()


async def get_current_user(
    authorization: Optional[str] = Header(None),
    auth_settings: AuthSettings = Depends(get_auth_settings),
):
    if authorization is None or not authorization.startswith('Bearer '):
        detail = 'missing from headers' if authorization is None else \
            'does not start with Bearer'
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Authorization {detail}',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    try:
        token = authorization.replace('Bearer ', '')
        header = jwt.get_unverified_header(token)
        async with httpx.AsyncClient() as client:
            resp = await client.get(auth_settings.jwks_uri)

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
