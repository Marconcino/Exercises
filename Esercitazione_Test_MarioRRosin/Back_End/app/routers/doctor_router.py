from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.db import SessionLocal
from app.schemas.doctor_schema import DoctorCreate, DoctorRead as DoctorResponse
from app.crud.doctor_crud import (
    create_doctor,
    get_all_doctors,
    get_doctor,
)

# Getting the database session
router = APIRouter(
    prefix = "/doctors",
    tags = ["Doctors"]
)


@router.post("/", response_model = DoctorResponse)
def create_new_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(SessionLocal)
):

    # Create a new doctor
    return create_doctor(
        db = db,
        full_name = doctor.full_name,
        specialization = doctor.specialization,
        availability = doctor.availability
    )


# Retrieve all doctors.
@router.get("/", response_model=List[DoctorResponse])
def read_all_doctors(db: Session = Depends(SessionLocal)):
    return get_all_doctors(db)

# Retrieve a doctor by ID
@router.get("/{doctor_id}", response_model = DoctorResponse)
def read_doctor(doctor_id: int, db: Session = Depends(SessionLocal)):
    doctor = get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail = "Doctor not found")
    return doctor
