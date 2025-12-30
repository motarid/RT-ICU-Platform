from sqlalchemy.orm import Session
from . import models, schemas

def create_patient(db: Session, payload: schemas.PatientCreate) -> models.Patient:
    patient = models.Patient(
        name=payload.name,
        age=payload.age,
        diagnosis=payload.diagnosis,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def list_patients(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Patient)
        .order_by(models.Patient.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def update_patient(db: Session, patient_id: int, payload: schemas.PatientUpdate):
    patient = get_patient(db, patient_id)
    if not patient:
        return None

    if payload.name is not None:
        patient.name = payload.name
    if payload.age is not None:
        patient.age = payload.age
    if payload.diagnosis is not None:
        patient.diagnosis = payload.diagnosis

    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int) -> bool:
    patient = get_patient(db, patient_id)
    if not patient:
        return False
    db.delete(patient)
    db.commit()
    return True
