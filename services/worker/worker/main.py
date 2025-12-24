import time
import logging
import os
import sys

def setup_logging():
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | worker | %(message)s",
        stream=sys.stdout,
    )
    logging.info("Worker logging initialized (level=%s)", level_name)

def main():
    setup_logging()
    while True:
        logging.info("heartbeat: worker is running")
        time.sleep(60)

if __name__ == "__main__":
    main()
