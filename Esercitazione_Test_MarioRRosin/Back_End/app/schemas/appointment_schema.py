# Appointment schemas for visiting rooms

from pydantic import BaseModel
from datetime import date, time


# Base
class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    visit_room_id: int
    date: date
    time: time
    visit_type: str
    duration_minutes: int


# CREATE
class AppointmentCreate(AppointmentBase):
    pass


# READ
class AppointmentRead(AppointmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True


# UPDATE (solo ciò che ha senso modificare)
class AppointmentUpdate(BaseModel):
    date: date | None = None
    time: time | None = None
    visit_room_id: int | None = None
    status: str | None = None
