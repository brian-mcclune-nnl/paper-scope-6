"""The dochunt-api main module.

"""

from functools import lru_cache
from typing import Optional

import httpx

from fastapi import FastAPI, Request, Header, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from pydantic import BaseModel, BaseSettings


class AuthSettings(BaseSettings):
    jwks_uri: str = (
        'https://clunacy.b2clogin.com/clunacy.onmicrosoft.com/'
        'discovery/v2.0/keys?p=b2c_1_dochunt_signupsignin'
    )
    b2c_client_id: str
    b2c_client_secret: str

    class Config:
        env_file = '.env'


class User(BaseModel):
    given_name: str
    family_name: str


app = FastAPI()

origins = [
    "https://localhost:3000",
    "https://localhost:3000/",
    "https://dochunt-vue3-spa.azurewebsites.net",
    "https://dochunt-vue3-spa.azurewebsites.net/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get('/')
async def root(request: Request, user: User = Depends(get_current_user)):
    return {
        'message': f'Hello {user} from FastAPI',
        'request_headers': request.headers,
    }
