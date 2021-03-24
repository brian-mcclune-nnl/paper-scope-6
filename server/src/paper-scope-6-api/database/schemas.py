"""The paper-scope-6-api model schemas."""

import datetime

from typing import List

from pydantic import BaseModel


class Article(BaseModel):
    id: int
    index: int
    href: str
    title: str
    description: str
    image: str
    tags: str
    groups: List[str]
    author: str
    date: datetime.datetime
    content: str
    similarity: float

    class Config:
        orm_mode = True
