from __future__ import annotations
import os
import psycopg
import psycopg.extras
from contextlib import contextmanager

def _dsn() -> str:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")
    return dsn

@contextmanager
def conn():
    c = psycopg.connect(_dsn(), cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield c.cursor()
        c.commit()
    finally:
        c.close()
