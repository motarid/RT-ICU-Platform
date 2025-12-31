from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Patient(Base):
    # CHANGED: Renamed to 'patients_v2' to fix the "Column not found" error
    __tablename__ = "patients_v2"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # This now matches your schema
    age = Column(Integer)
    diagnosis = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
