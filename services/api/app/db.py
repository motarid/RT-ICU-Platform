import os
from contextlib import contextmanager

try:
    import psycopg2
except Exception:
    psycopg2 = None


def _dsn() -> str:
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")
    return dsn


@contextmanager
def conn():
    if psycopg2 is None:
        raise RuntimeError("psycopg2 is not installed")

    c = psycopg2.connect(_dsn())
    try:
        cur = c.cursor()
        yield cur
        c.commit()
    finally:
        c.close()
def init_db():
    with conn() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                diagnosis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
def ensure_patients_table():
    with conn() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                full_name TEXT NOT NULL,
                mrn TEXT,
                age INTEGER,
                diagnosis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
