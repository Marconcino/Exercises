# Patien schemas for 

from pydantic import BaseModel, EmailStr
from datetime import date


# Base
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    email: EmailStr
    phone_number: str
    emergency_contact: str | None = None


# CREATE
class PatientCreate(PatientBase):
    pass


# UPDATE
class PatientUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    emergency_contact: str | None = None


# READ
class PatientRead(PatientBase):
    id: int

    class Config:
        from_attributes = True
