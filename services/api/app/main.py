import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_config import setup_logging
from app.health import router as health_router
from app.review_notify import router as review_notify_router

setup_logging()
logger = logging.getLogger("rticu-api")

app = FastAPI(title="RTICU API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(review_notify_router)

logger.info("API started")
