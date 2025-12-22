from __future__ import annotations

import os
import psycopg
from contextlib import contextmanager


def _dsn() -> str:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")
    return dsn


@contextmanager
def conn():
    with psycopg.connect(_dsn(), row_factory=psycopg.rows.dict_row) as c:
        with c.cursor() as cur:
            yield cur
        c.commit()
