import os
import logging
from logging.config import dictConfig

def setup_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()

    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            }
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "default"}
        },
        "root": {"level": level, "handlers": ["console"]},
        "loggers": {
            "uvicorn": {"level": level, "handlers": ["console"], "propagate": False},
            "uvicorn.error": {"level": level, "handlers": ["console"], "propagate": False},
            "uvicorn.access": {"level": level, "handlers": ["console"], "propagate": False},
        },
    })

    logging.getLogger("rticu-api").info("Logging configured (LOG_LEVEL=%s)", level)
