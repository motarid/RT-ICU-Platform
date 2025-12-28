import logging
from pydantic import BaseModel
from typing import Optional
from app.db import ensure_patients_table

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
class PatientCreate(BaseModel):
    full_name: str
    mrn: Optional[str] = None
    age: Optional[int] = None
    diagnosis: Optional[str] = None


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
@app.post("/patients/init")
def patients_init():
    ensure_patients_table()
    return {"ok": True, "message": "patients table ready"}
@app.post("/patients")
def create_patient(p: PatientCreate):
    ensure_patients_table()
    try:
        from app.db import conn as db_conn
        with db_conn() as cur:
            cur.execute(
                """
                INSERT INTO patients (full_name, mrn, age, diagnosis)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (p.full_name, p.mrn, p.age, p.diagnosis),
            )
            new_id = cur.fetchone()[0]
        return {"ok": True, "id": new_id}
    except Exception:
        return {"ok": False, "message": "failed to create patient"}
@app.get("/patients")
def list_patients():
    ensure_patients_table()
    try:
        from app.db import conn as db_conn
        with db_conn() as cur:
            cur.execute(
                """
                SELECT id, full_name, mrn, age, diagnosis, created_at
                FROM patients
                ORDER BY id DESC
                LIMIT 20;
                """
            )
            rows = cur.fetchall()

        items = []
        for r in rows:
            items.append(
                {
                    "id": r[0],
                    "full_name": r[1],
                    "mrn": r[2],
                    "age": r[3],
                    "diagnosis": r[4],
                    "created_at": str(r[5]),
                }
            )
        return {"ok": True, "items": items}
    except Exception:
        return {"ok": False, "items": []}


# --- Routers ---
app.include_router(health_router)
app.include_router(review_notify_router)

from app.db import init_db

@app.get("/db/init")
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
