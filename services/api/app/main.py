from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.cors import get_allowed_origins

from app.db.session import engine
from app.db.base import Base

from app.models.patient import Patient  # noqa: F401
from app.routers.health import router as health_router
from app.routers.patients import router as patients_router

logger = setup_logging("rticu-api")

app = FastAPI(title=settings.APP_NAME)

# ✅ CORS
origins = get_allowed_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create DB tables (مؤقتًا — لاحقًا Alembic)
Base.metadata.create_all(bind=engine)

# ✅ Routers
app.include_router(health_router)
app.include_router(patients_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "RT-ICU API running"}
