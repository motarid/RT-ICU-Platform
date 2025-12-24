from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger("health")

@router.get("/health")
def health_check():
    logger.info("Health endpoint was called")
    return {"status": "ok"}
