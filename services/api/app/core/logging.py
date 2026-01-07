import logging
import os

def setup_logging(service_name: str = "rticu-api"):
    level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logger = logging.getLogger(service_name)
    logger.info("Logging initialized (level=%s)", level)
    return logger
