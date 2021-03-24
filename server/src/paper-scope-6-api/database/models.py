"""The paper-scope-6-api database models."""

import sqlalchemy as sa

from . import Base


class Article(Base):
    __tablename__ = 'article'

    id = sa.Column(sa.Integer, primary_key=True)
    index = sa.Column(sa.Integer)
    href = sa.Column(sa.String(256))
    title = sa.Column(sa.String(256))
    description = sa.Column(sa.String(1024))
    image = sa.Column(sa.String(512))
    tags = sa.Column(sa.String(512))
    groups = sa.Column(sa.String(512))
    author = sa.Column(sa.String(64))
    date = sa.Column(sa.DateTime)
    content = sa.Column(sa.String(None))

    def __repr__(self):
        return (
            f'Article(id={self.id!r}, href={self.href!r}, title={self.title!r}'
            f', description={self.description[:30]!r}, image={self.image!r}'
            f', tags={self.tags!r}, groups={self.groups!r}'
            f', author={self.author!r}, date={self.date!r}'
            f', content={self.content[:30]!r}'
        )
