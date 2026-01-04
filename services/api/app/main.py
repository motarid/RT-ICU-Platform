import os
import logging
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_
from typing import List

from .database import Base, engine, get_db
from . import models, schemas, crud

# ---------- Logging ----------
logger = logging.getLogger("rticu-api")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | rticu-api | %(message)s"
)

app = FastAPI(title="RT-ICU Platform API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok", "message": "RT-ICU API running"}

@app.get("/health")
def health():
    return {"ok": True}

# -------------------------
# Patients (SERVER-SIDE pagination + sorting + search)
# -------------------------
@app.get("/patients")
def list_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("name"),       # name | age | diagnosis
    sort_dir: str = Query("asc"),        # asc | desc
    q: str | None = Query(None),         # search text
    db: Session = Depends(get_db),
):
    query = db.query(models.Patient)

    # Search
    if q:
        like = f"%{q.lower()}%"
        query = query.filter(
            or_(
                models.Patient.name.ilike(like),
                models.Patient.diagnosis.ilike(like),
                models.Patient.age.cast(str).ilike(like),
            )
        )

    # Sorting
    sort_column = {
        "name": models.Patient.name,
        "age": models.Patient.age,
        "diagnosis": models.Patient.diagnosis,
    }.get(sort_by, models.Patient.name)

    if sort_dir == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # Total count (before pagination)
    total = query.count()

    # Pagination
    items = (
        query
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
    }

# باقي CRUD (POST/PUT/DELETE) تبقى كما هي
@app.post("/patients", response_model=schemas.PatientOut)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = crud.create_patient(db, payload)
    return patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_patient(db, patient_id)
    return {"ok": ok, "deleted_id": patient_id}
