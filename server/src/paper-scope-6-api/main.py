"""The paper-scope-6-api main module.

"""

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .dependencies import get_current_user


app = FastAPI()

origins = [
    "https://localhost:3000",
    "https://localhost:3000/",
    "https://paper-scope-6.azurewebsites.net",
    "https://paper-scope-6.azurewebsites.net/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    given_name: str
    family_name: str


@app.get('/')
async def root(request: Request, user: User = Depends(get_current_user)):
    username = f'{user["given_name"]} {user["family_name"]}'
    return {
        'message': f'Hello {username} from FastAPI',
        'request_headers': request.headers,
    }
