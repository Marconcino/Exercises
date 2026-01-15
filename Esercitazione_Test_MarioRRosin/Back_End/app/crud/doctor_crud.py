# CRUD operations for Doctor model

from sqlalchemy.orm import Session
from app.models.doctor import Doctor


# CREATE
def create_doctor( db: Session, full_name: str, specialization: str, availability: str) -> Doctor:
    # Create a new doctor
    doctor = Doctor(full_name = full_name, specialization = specialization, availability = availability)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

# READ
def get_doctor(db: Session, doctor_id: int) -> Doctor | None:
    # Get the info of a doctor by ID
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_all_doctors(db: Session, skip: int = 0, limit: int = 100) -> list[Doctor]:
    # Retrieve all doctors with pagination
    return db.query(Doctor).offset(skip).limit(limit).all()

# UPDATE
def update_doctor(db: Session, doctor_id: int, first_name: str | None = None, last_name: str | None = None, 
                  specialization: str | None = None,
                  availability: str | None = None) -> Doctor | None:
    doctor = get_doctor(db, doctor_id)
    if not doctor:
        return None

    if first_name is not None:
        doctor.first_name = first_name
    if last_name is not None:
        doctor.last_name = last_name
    if specialization is not None:
        doctor.specialization = specialization
    if availability is not None:
        doctor.availability = availability

    db.commit()
    db.refresh(doctor)
    return doctor


# DELETE
def delete_doctor(db: Session, doctor_id: int) -> bool:
    # Delete a doctor by ID
    doctor = get_doctor(db, doctor_id)
    if not doctor:
        return False

    db.delete(doctor)
    db.commit()
    return True