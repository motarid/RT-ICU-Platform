import os
import time
import logging
from fastapi import APIRouter

import psycopg2

router = APIRouter()
logger = logging.getLogger("health")

def check_db():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        return False, "DATABASE_URL is not set"

    start = time.time()
    try:
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        ms = int((time.time() - start) * 1000)
        return True, f"db ok ({ms}ms)"
    except Exception as e:
        return False, f"db error: {type(e).__name__}: {e}"

@router.get("/health")
def health():
    ok_db, db_msg = check_db()

    if ok_db:
        logger.info(f"HEALTH OK | {db_msg}")
        return {"status": "ok", "db": "ok", "detail": db_msg}
    else:
        logger.error(f"HEALTH FAIL | {db_msg}")
        # نرجّع status=500 حتى Render/المراقبة تعرف أن الخدمة غير سليمة
        return {"status": "fail", "db": "fail", "detail": db_msg}
