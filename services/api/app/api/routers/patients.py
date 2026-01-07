from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.patient import PatientCreate, PatientUpdate, PatientOut
from app.crud import patient as patient_crud

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("", response_model=PatientOut)
def create(payload: PatientCreate, db: Session = Depends(get_db)):
    return patient_crud.create_patient(db, payload)

@router.get("", response_model=List[PatientOut])
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return patient_crud.list_patients(db, skip=skip, limit=limit)

@router.get("/{patient_id}", response_model=PatientOut)
def get_one(patient_id: int, db: Session = Depends(get_db)):
    p = patient_crud.get_patient(db, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@router.put("/{patient_id}", response_model=PatientOut)
def update(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    p = patient_crud.update_patient(db, patient_id, payload)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@router.delete("/{patient_id}")
def delete(patient_id: int, db: Session = Depends(get_db)):
    ok = patient_crud.delete_patient(db, patient_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"ok": True, "deleted_id": patient_id}
