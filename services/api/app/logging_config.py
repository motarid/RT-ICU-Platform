import logging
import os
import sys

def setup_logging(service_name: str = "rticu-api") -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    root.setLevel(level)

    # Prevent duplicate handlers (e.g., reloads)
    if root.handlers:
        return logging.getLogger(service_name)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # Uvicorn log levels
    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)

    logger = logging.getLogger(service_name)
    logger.info("Logging initialized (level=%s)", level_name)
    return logger
