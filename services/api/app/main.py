import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_config import setup_logging
from app.health import router as health_router
from app.review_notify import router as review_notify_router

# DB (Neon/Postgres) optional ping endpoint
from app.db import conn as db_conn


# --- Logging ---
setup_logging()
logger = logging.getLogger("rticu-api")


# --- App ---
app = FastAPI(title="RTICU API", version="1.0.0")


# --- CORS (مفتوح الآن للتجربة؛ لاحقًا ضيّقه على دومين الواجهة فقط) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Root (يعالج طلبات Render HEAD/GET ويمنع مشاكل 404/405) ---
@app.api_route("/", methods=["GET", "HEAD"], operation_id="root_status")
def root():
    return {
        "service": "rticu-api",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "db_ping": "/db/ping",
    }


# --- Routers ---
app.include_router(health_router)
app.include_router(review_notify_router)

from app.db import init_db

@app.post("/db/init")
def init_database():
    init_db()
    return {"status": "ok", "message": "Database initialized"}

# --- DB Ping (اختبار اتصال Neon) ---
@app.get("/db/ping", operation_id="db_ping")
def db_ping():
    """
    يرجّع OK إذا كانت قاعدة البيانات متصلة.
    يعتمد على DATABASE_URL في Render Environment.
    """
    try:
        with db_conn() as cur:
            cur.execute("SELECT 1;")
            value = cur.fetchone()[0]
        return {"ok": True, "db": "connected", "result": value}
    except Exception as e:
        logger.exception("DB ping failed")
        # لا تُظهر تفاصيل حساسة للعميل
        return {"ok": False, "db": "error", "message": "Database connection failed"}


logger.info("API started")
