from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/health")
def health():
    # Render health check should be FAST and RELIABLE.
    # Do not block on DB here; just confirm config existence.
    has_db = bool(os.getenv("DATABASE_URL"))
    return {"ok": True, "service": "rticu-api", "db_configured": has_db}
