"""The paper-scope-6-api database package."""

from functools import lru_cache
from typing import Generator
from urllib.parse import quote_plus

from pydantic import BaseSettings
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class DbSettings(BaseSettings):
    db_passwd: str

    class Config:
        env_file = '.env.local'

    def __hash__(self):
        return hash(tuple(item for item in self.dict().items()))


@lru_cache
def get_db_settings():
    return DbSettings()


def get_connection_string(db_settings: DbSettings):
    your_password_here = db_settings.db_passwd
    conn_str = (
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=tcp:paper-scope-dbserver.database.windows.net,1433;'
        'Database=paper-scope-db;'
        'Uid=brian;'
        f'Pwd={your_password_here};'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=60;'
    )
    params = quote_plus(conn_str)
    return f'mssql+pyodbc:///?odbc_connect={params}'


SessionLocal = sessionmaker(create_engine(get_connection_string(DbSettings())))


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
