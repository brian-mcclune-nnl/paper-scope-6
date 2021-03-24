"""The paper-scope-6-api database CRUD functions."""

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import case

from .models import Article


def get_article_by_id(db: Session, art_id: int):
    return db.query(Article).filter(Article.id == art_id).first()


def get_articles_by_indices(db: Session, indices: List[int]):
    ordering = case(
        {index: i for i, index in enumerate(indices)},
        value=Article.index,
    )
    return db.query(Article).filter(
        Article.index.in_(indices)).order_by(ordering).all()
