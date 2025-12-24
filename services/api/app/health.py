from fastapi import APIRouter
import os
import logging

router = APIRouter()
logger = logging.getLogger("rticu-api")

@router.get("/health")
def health():
    # لا تفشل الخدمة إذا DB غير جاهزة
    has_db = bool(os.getenv("DATABASE_URL"))
    return {"ok": True, "service": "rticu-api", "db_configured": has_db}
