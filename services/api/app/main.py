import os
import logging
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_
from typing import Optional

from .database import Base, engine, get_db
from . import models, schemas, crud

# ---------- Logging ----------
logger = logging.getLogger("rticu-api")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | rticu-api | %(message)s"
)

app = FastAPI(title="RT-ICU Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok", "message": "RT-ICU API running"}

@app.get("/health")
def health():
    return {"ok": True}

# -------------------------
# Patients (server-side pagination + sorting + search + advanced filters)
# -------------------------
@app.get("/patients")
def list_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),

    sort_by: str = Query("name"),        # name | age | diagnosis
    sort_dir: str = Query("asc"),        # asc | desc

    q: Optional[str] = Query(None),      # free text search
    age_min: Optional[int] = Query(None, ge=0, le=130),
    age_max: Optional[int] = Query(None, ge=0, le=130),

    # diagnosis can be: "ARDS" or "ARDS,COPD"
    diagnosis: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query_obj = db.query(models.Patient)

    # Free text search
    if q:
        like = f"%{q.lower()}%"
        query_obj = query_obj.filter(
            or_(
                models.Patient.name.ilike(like),
                models.Patient.diagnosis.ilike(like),
            )
        )

    # Age range filters
    if age_min is not None:
        query_obj = query_obj.filter(models.Patient.age >= age_min)
    if age_max is not None:
        query_obj = query_obj.filter(models.Patient.age <= age_max)

    # Diagnosis multi-filter (CSV)
    if diagnosis:
        diag_list = [d.strip() for d in diagnosis.split(",") if d.strip()]
        if diag_list:
            # match any of selected diagnoses
            like_filters = [models.Patient.diagnosis.ilike(f"%{d}%") for d in diag_list]
            query_obj = query_obj.filter(or_(*like_filters))

    # Sorting
    sort_column = {
        "name": models.Patient.name,
        "age": models.Patient.age,
        "diagnosis": models.Patient.diagnosis,
    }.get(sort_by, models.Patient.name)

    query_obj = query_obj.order_by(desc(sort_column) if sort_dir == "desc" else asc(sort_column))

    # Total count
    total = query_obj.count()

    # Pagination
    items = (
        query_obj
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

# -------------------------
# CRUD (Create / Delete)
# -------------------------
@app.post("/patients", response_model=schemas.PatientOut)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, payload)

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_patient(db, patient_id)
    return {"ok": ok, "deleted_id": patient_id}
