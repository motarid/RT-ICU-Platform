import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_config import setup_logging
from app.health import router as health_router
from app.review_notify import router as review_notify_router

setup_logging()
logger = logging.getLogger("rticu-api")

app = FastAPI(title="RTICU API", version="1.0.0")

logger.info("RT-ICU API starting...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(review_notify_router)

# Optional: log any unhandled exception in a clean way
@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    raise
