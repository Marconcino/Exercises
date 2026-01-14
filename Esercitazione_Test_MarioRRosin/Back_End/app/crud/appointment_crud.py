from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.appointment import Appointment


# CREATE
def create_appointment(db: Session, doctor_id: int, patient_id: int, visit_room_id: int, date, time, visit_type: str, duration_minutes: int) -> Appointment:
    appointment = Appointment(doctor_id = doctor_id, patient_id = patient_id, visit_room_id = visit_room_id, date = date, 
                              time = time, visit_type = visit_type, duration_minutes = duration_minutes, status = "scheduled")
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


# READ
def get_appointment(db: Session, appointment_id: int) -> Appointment | None:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments_by_patient(
    db: Session,
    patient_id: int
) -> list[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .all()
    )


def get_appointments_by_doctor_and_date(
    db: Session,
    doctor_id: int,
    date
) -> list[Appointment]:
    return (
        db.query(Appointment)
        .filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == date
            ) # With and_ we can filter multiple conditions 
        )
        .all() # This one has the task to return all the appointments that match the filter
    )


# UPDATE
def update_appointment_status(
    db: Session,
    appointment_id: int,
    status: str
) -> Appointment | None:
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return None

    appointment.status = status
    db.commit()
    db.refresh(appointment)
    return appointment


# DELETE (soft delete)
def cancel_appointment(db: Session, appointment_id: int) -> bool:
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return False

    appointment.status = "cancelled"
    db.commit()
    return True