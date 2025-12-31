from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PatientCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=120)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    diagnosis: Optional[str] = Field(default=None, max_length=300)

class PatientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=120)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    diagnosis: Optional[str] = Field(default=None, max_length=300)

class PatientOut(BaseModel):
    id: int
    name: str
    age: Optional[int]
    diagnosis: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
