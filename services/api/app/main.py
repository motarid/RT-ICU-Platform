import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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

# Create tables (OK for now; later you can move to migrations)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok", "message": "RT-ICU API running"}

@app.get("/health")
def health():
    return {"ok": True}

# -------------------------
# Patients CRUD
# -------------------------

@app.post("/patients", response_model=schemas.PatientOut)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    try:
        patient = crud.create_patient(db, payload)
        return patient
    except Exception as e:
        logger.exception("Create patient failed")
        raise HTTPException(status_code=500, detail="Failed to create patient")

@app.get("/patients", response_model=List[schemas.PatientOut])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_patients(db, skip=skip, limit=limit)

@app.get("/patients/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", response_model=schemas.PatientOut)
def update_patient(patient_id: int, payload: schemas.PatientUpdate, db: Session = Depends(get_db)):
    patient = crud.update_patient(db, patient_id, payload)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_patient(db, patient_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"ok": True, "deleted_id": patient_id}
