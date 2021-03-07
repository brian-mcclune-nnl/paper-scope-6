"""Router module to define `/search` routes.

"""

import json
import pathlib

from fastapi import APIRouter

router = APIRouter(prefix='/search', tags=['search'])


@router.get('/')
async def search():
    matches = pathlib.Path(__file__).parent.parent.joinpath('matches.json')
    with open(matches) as jsonf:
        return json.load(jsonf)
