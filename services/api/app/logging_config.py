import logging
import os
import sys

def setup_logging() -> None:
    """
    Production-friendly logging for Render.
    - No extra libraries.
    - Logs to stdout so Render can capture them.
    - Respects LOG_LEVEL env var (default INFO).
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()

    # Avoid duplicate handlers on reloads
    if root.handlers:
        root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(handler)

    # Make uvicorn logs consistent
    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)
