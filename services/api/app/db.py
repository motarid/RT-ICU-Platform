from __future__ import annotations
import os
import psycopg2
import psycopg2.extras
from contextlib import contextmanager

def _dsn() -> str:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")
    return dsn

@contextmanager
def conn():
    c = psycopg2.connect(_dsn(), cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield c.cursor()
        c.commit()
    finally:
        c.close()
