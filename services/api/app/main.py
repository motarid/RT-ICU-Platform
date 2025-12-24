from app.logging_config import setup_logging
logger = setup_logging("rticu-api")

from fastapi import FastAPI@app.get("/")
def root():
    logger.info("API starting...")

    return {
        "service": "rticu-api",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

from fastapi.middleware.cors import CORSMiddleware
import logging

from app.logging_config import setup_logging
from app.health import router as health_router
app.include_router(health_router)
from app.review_notify import router as review_notify_router

# ---- Logging ----
setup_logging()
logger = logging.getLogger("rticu-api")

# ---- App ----
app = FastAPI(
    title="RT-ICU API",
    version="1.0.0"
)

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Root Endpoint (يحل مشكلة 404) ----
@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "service": "rticu-api",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

# ---- Routers ----
app.include_router(health_router)
app.include_router(review_notify_router)

logger.info("RT-ICU API started successfully")
