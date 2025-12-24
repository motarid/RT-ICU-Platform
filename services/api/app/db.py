import os
import psycopg
from contextlib import contextmanager

def _dsn() -> str:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")
    return dsn

@contextmanager
def get_connection():
    """
    psycopg v3 connection context manager
    Usage:
        with get_connection() as conn:
            with conn.cursor() as cur:
                ...
    """
    conn = psycopg.connect(_dsn())
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
