import time
import logging
from worker.logging_config import setup_logging
from worker.db import conn

setup_logging()
logger = logging.getLogger("rticu-worker")

def run_forever():
    logger.info("Worker started")
    while True:
        try:
            with conn() as cur:
                cur.execute("SELECT 1;")
            logger.info("Worker heartbeat OK")
        except Exception:
            logger.exception("Worker error")
        time.sleep(30)

if __name__ == "__main__":
    run_forever()
