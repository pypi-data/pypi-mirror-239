import sqlalchemy
from sqlalchemy import text

from puddl.typing import URL


def list_databases(url: URL):
    engine = sqlalchemy.create_engine(url)
    with engine.connect() as conn:
        return [row[0] for row in conn.execute(text('SELECT datname FROM pg_catalog.pg_database')).fetchall()]


def list_schemas(url: URL):
    engine = sqlalchemy.create_engine(url)
    inspection_result = sqlalchemy.inspect(engine)
    return inspection_result.get_schema_names()
