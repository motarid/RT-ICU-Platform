import os
import psycopg
import logging

logger = logging.getLogger("rticu-api.db")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

def get_connection():
    try:
        return psycopg.connect(DATABASE_URL)
    except Exception as e:
        logger.error("Database connection failed", exc_info=e)
        raise
