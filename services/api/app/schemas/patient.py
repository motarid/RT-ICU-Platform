from pydantic import BaseModel, Field

class PatientCreate(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(gt=0, lt=130)
    diagnosis: str = Field(min_length=1)

class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = Field(default=None, gt=0, lt=130)
    diagnosis: str | None = None

class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    diagnosis: str

    class Config:
        from_attributes = True
