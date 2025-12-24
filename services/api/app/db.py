import os
import psycopg2
from contextlib import contextmanager

def _dsn() -> str:
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")
    return dsn

@contextmanager
def conn():
    connection = psycopg2.connect(_dsn())
    try:
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        finally:
            cursor.close()
    finally:
        connection.close()
