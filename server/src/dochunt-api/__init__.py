"""The dochunt-api main module.

"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "https://localhost:3000/",
    "https://icy-wave-07ae5a40f.azurestaticapps.net/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root(request: Request):
    return {
        'message': 'Hello World from FastAPI',
        'request_headers': request.headers,
    }
