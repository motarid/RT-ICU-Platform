from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.core.cors import get_allowed_origins
from app.core.config import settings

from app.db.session import engine
from app.db.base import Base

from app.api.routers.health import router as health_router
from app.api.routers.patients import router as patients_router

logger = setup_logging("rticu-api")

app = FastAPI(title=settings.APP_NAME)

# ✅ CORS (حل مشكلة المتصفح)
origins = get_allowed_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create tables (مؤقتًا، لاحقًا Alembic migrations)
Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(patients_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "RT-ICU API running"}
