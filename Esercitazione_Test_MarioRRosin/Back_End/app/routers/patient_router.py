from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.db import SessionLocal
from app.schemas.patient_schema import PatientCreate, PatientRead as PatientResponse
from app.crud.patient_crud import (
    create_patient,
    get_patient,
    get_patients,
    get_patient_by_email
)

router = APIRouter(
    prefix = "/patients",
    tags = ["Patients"]
)

# POST
@router.post("/", response_model = PatientResponse)
def create_new_patient(
    patient: PatientCreate,
    db: Session = Depends(SessionLocal)
):
    # Create a new patient.
    return create_patient(db, patient)

# GET
# Retrieve all patients.
@router.get("/", response_model = List[PatientResponse])
def read_all_patients(db: Session = Depends(SessionLocal)):
    return get_patients(db)

# Retrieve patient details by ID
@router.get("/{patient_id}", response_model = PatientResponse)
def read_patient(patient_id: int, db: Session = Depends(SessionLocal)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code = 404, detail = "No Patient found with the email")
    return patient
