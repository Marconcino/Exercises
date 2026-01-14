from sqlalchemy.orm import Session
from app.models.patient import Patient


# CREATE
def create_patient(db: Session, first_name: str, last_name: str, birth_date, email: str, phone_number: str, emergency_contact: str | None = None) -> Patient:
    patient = Patient(first_name = first_name,
        last_name = last_name,
        birth_date = birth_date,
        email = email,
        phone_number = phone_number,
        emergency_contact = emergency_contact
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

# READ
def get_patient(db: Session, patient_id: int) -> Patient | None:
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patient_by_email(db: Session, email: str) -> Patient | None:
    return db.query(Patient).filter(Patient.email == email).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> list[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()


# UPDATE
def update_patient(db: Session, patient_id: int, first_name: str | None = None,
                last_name: str | None = None, phone_number: str | None = None, 
                emergency_contact_name: str | None = None, emergency_contact_phone: str | None = None) -> Patient | None:
    patient = get_patient(db, patient_id)
    if not patient:
        return None

    if first_name is not None:
        patient.first_name = first_name
    if last_name is not None:
        patient.last_name = last_name
    if phone_number is not None:
        patient.phone_number = phone_number
    if emergency_contact_name is not None:
        patient.emergency_contact_name = emergency_contact_name
    if emergency_contact_phone is not None:
        patient.emergency_contact_phone = emergency_contact_phone

    db.commit()
    db.refresh(patient)
    return patient


# DELETE
def delete_patient(db: Session, patient_id: int) -> bool:
    patient = get_patient(db, patient_id)
    if not patient:
        return False

    db.delete(patient)
    db.commit()
    return True