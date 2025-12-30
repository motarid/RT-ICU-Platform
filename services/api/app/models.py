from sqlalchemy import Column, Integer, Text, DateTime, func
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    age = Column(Integer, nullable=True)
    diagnosis = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
