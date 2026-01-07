from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

def create_patient(db: Session, payload: PatientCreate) -> Patient:
    p = Patient(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def list_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patient).offset(skip).limit(limit).all()

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def update_patient(db: Session, patient_id: int, payload: PatientUpdate):
    p = get_patient(db, patient_id)
    if not p:
        return None
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

def delete_patient(db: Session, patient_id: int) -> bool:
    p = get_patient(db, patient_id)
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True
