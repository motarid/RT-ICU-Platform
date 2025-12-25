from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_config import setup_logging
from app.health import router as health_router
from app.review_notify import router as review_notify_router

logger = setup_logging("rticu-api")

app = FastAPI(title="RTICU API", version="1.0.0")


# Optional but recommended: remove 404 at "/"
@app.get("/")
def root():
    return {
        "service": "rticu-api",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


# CORS (keep as you had it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health_router)
app.include_router(review_notify_router)

logger.info("API startup configuration complete.")
