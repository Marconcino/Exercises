from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.db import SessionLocal
from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentRead as AppointmentResponse
)
from app.crud.appointment_crud import (
    create_appointment,
    get_appointment,
    get_appointments_by_patient,
    cancel_appointment,
    update_appointment_status
)

router = APIRouter(
    prefix = "/appointments",
    tags = ["Appointments"]
)

# GET
@router.get("/{appointment_id}", response_model = AppointmentResponse)
def read_appointment(
    appointment_id: int,
    db: Session = Depends(SessionLocal)
): 
    # Retrieve appointment details
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail = "Appointment not found")
    return appointment


@router.get("/patient/{patient_id}", response_model = List[AppointmentResponse])
def read_patient_appointments(
    patient_id: int,
    db: Session = Depends(SessionLocal)
):
    # Retrieve appointment history for a patient
    return get_appointments_by_patient(db, patient_id)

# POST
@router.post("/", response_model=AppointmentResponse)
def book_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(SessionLocal)
):
    # Book a new appointment after checking doctor and room availability
    return create_appointment(db, appointment)


# PUT
@router.put("/{appointment_id}", response_model = AppointmentResponse)
def modify_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(SessionLocal)
):
    # Modify an existing appointment (date, time, type)
    updated = update_appointment_status(db, appointment_id, appointment)
    if not updated:
        raise HTTPException(status_code = 400, detail = "Appointment cannot be modified")
    return updated

# DELETE
@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(SessionLocal)
):
    # Cancel an appointment with minimum notice
    success = cancel_appointment(db, appointment_id)
    if not success:
        raise HTTPException(status_code = 400, detail = "Appointment cannot be cancelled")
    return {"message": "Appointment cancelled successfully"}



