# BOOKING CRUD
# This CRUD module provides functions to create, read, update, and delete Booking records in the database

from sqlalchemy.orm import Session
from sqlalchemy import and_ # and_ is used to apply multiple filter conditions
from sqlalchemy.exc import IntegrityError
from datetime import date, time
from app.models.booking import Booking, BookingStatus, DayOfWeek

# CREATE
def create_booking(db: Session, client_id: int, table_id: int, reservation_date: date, reservation_time: time, 
                   day_of_week: DayOfWeek, guest_count: int, status: BookingStatus = BookingStatus.pending
) -> Booking:
    booking = Booking(client_id = client_id, table_id = table_id, reservation_date = reservation_date, 
                      reservation_time = reservation_time, day_of_week = day_of_week, 
                      guest_count = guest_count, status = status)

    db.add(booking)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # DB may raise due to:
        # - UNIQUE ux_table_date_time (double booking)
        # - FK constraints (client/table not found)
        raise

    db.refresh(booking)
    return booking


# READ
def get_booking(db: Session, booking_id: int) -> Booking | None:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings(db: Session) -> list[Booking]:
    return db.query(Booking).all()

def get_bookings_by_client(db: Session, client_id: int) -> list[Booking]:
    return (
        db.query(Booking)
        .filter(Booking.client_id == client_id)
        .all()
    )

def get_bookings_by_table_and_date(
    db: Session,
    table_id: int,
    reservation_date: date
) -> list[Booking]:
    return (
        db.query(Booking)
        .filter(
            and_(
                Booking.table_id == table_id,
                Booking.reservation_date == reservation_date
            )  # Here we use and_ to filter multiple conditions
        )
        .all()
    )

def get_bookings_by_date_time(
    db: Session,
    reservation_date: date,
    reservation_time: time
) -> list[Booking]:
    return (
        db.query(Booking)
        .filter(
            and_(
                Booking.reservation_date == reservation_date,
                Booking.reservation_time == reservation_time
            )
        )
        .all()
    )


# UPDATE
def update_booking_status(
    db: Session,
    booking_id: int,
    status: BookingStatus
) -> Booking | None:
    booking = get_booking(db, booking_id)
    if not booking:
        return None

    booking.status = status
    db.commit()
    db.refresh(booking)
    return booking


# reservation_date and reservation_time are typed as:
# - datetime.date / datetime.time in Python
# - DATE / TIME in MySQL
# This mapping avoids Pylance errors when assigning values in CRUD operations
def update_booking_details(
    db: Session,
    booking_id: int,
    table_id: int | None = None,
    reservation_date: date | None = None,
    reservation_time: time | None = None,
    day_of_week: DayOfWeek | None = None,
    guest_count: int | None = None
) -> Booking | None:
    booking = get_booking(db, booking_id)
    if not booking:
        return None

    if table_id is not None:
        booking.table_id = table_id
    if reservation_date is not None:
        booking.reservation_date = reservation_date
    if reservation_time is not None:
        booking.reservation_time = reservation_time
    if day_of_week is not None:
        booking.day_of_week = day_of_week
    if guest_count is not None:
        booking.guest_count = guest_count

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Can fail for UNIQUE constraint or FK RESTRICT
        raise

    db.refresh(booking)
    return booking


# DELETE (soft delete like your example)
def cancel_booking(db: Session, booking_id: int) -> bool:
    booking = get_booking(db, booking_id)
    if not booking:
        return False

    booking.status = BookingStatus.cancelled
    db.commit()
    return True
