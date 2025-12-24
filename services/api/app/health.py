import logging
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger("rticu-api")

@router.get("/health")
def health():
    logger.info("Healthcheck hit")
    return {"status": "ok"}
