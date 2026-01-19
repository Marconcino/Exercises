# BOOKING ROUTER
# This router handles API endpoints related to bookings 

from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database.db import get_db
from app.schemas.booking_schema import BookingCreate, BookingUpdate, BookingRead as BookingResponse
from app.crud.booking_crud import (create_booking, get_booking, get_bookings, get_bookings_by_client, get_bookings_by_table_and_date, 
                                   update_booking_details, update_booking_status, cancel_booking)
from app.models.booking import BookingStatus, DayOfWeek


def _day_of_week_from_date(reservation_date: date) -> DayOfWeek:
    days = [
        DayOfWeek.Monday,
        DayOfWeek.Tuesday,
        DayOfWeek.Wednesday,
        DayOfWeek.Thursday,
        DayOfWeek.Friday,
        DayOfWeek.Saturday,
        DayOfWeek.Sunday,
    ]
    return days[reservation_date.weekday()]

router = APIRouter(prefix = "/bookings", tags = ["Bookings"])


# GET all bookings
@router.get("/", response_model=List[BookingResponse])
def read_bookings(db: Session = Depends(get_db)):
    return get_bookings(db)

# GET booking by ID
@router.get("/{booking_id}", response_model = BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Booking not found")
    return booking

# GET bookings by client ID
@router.get("/client/{client_id}", response_model = List[BookingResponse])
def read_bookings_for_client(client_id: int, db: Session = Depends(get_db)):
    return get_bookings_by_client(db, client_id)

# IMPORTANT: reservation_date is required here
@router.get("/table/{table_id}", response_model = List[BookingResponse])
def read_bookings_for_table(table_id: int, reservation_date: date, db: Session = Depends(get_db)):
    return get_bookings_by_table_and_date(db, table_id, reservation_date)


# POST
    # Creates a booking
    # - Returns Error 409 if the same table is already booked for the same date and time (double booking)
@router.post("/", response_model=BookingResponse, status_code = status.HTTP_201_CREATED)
def create_new_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    day_of_week = _day_of_week_from_date(payload.reservation_date)
    status_value = BookingStatus.pending
    if payload.status is not None:
        try:
            status_value = BookingStatus(payload.status)
        except ValueError:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = "Invalid status value",
            )
    try:
        return create_booking(
            db,
            client_id = payload.client_id,
            table_id = payload.table_id,
            reservation_date = payload.reservation_date,
            reservation_time = payload.reservation_time,
            day_of_week = day_of_week,
            guest_count = payload.guest_count,
            status = status_value,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Double booking: the selected table is already booked for that date and time",
        )


# PUT (full update)
    # Updates a booking.
    # - Returns 409 if update causes a double booking (same table/date/time slot)
@router.put("/{booking_id}", response_model = BookingResponse)
def modify_booking(booking_id: int, payload: BookingUpdate, db: Session = Depends(get_db)):
    day_of_week = None
    if payload.reservation_date is not None:
        day_of_week = _day_of_week_from_date(payload.reservation_date)
    try:
        updated = update_booking_details(
            db,
            booking_id,
            table_id=payload.table_id,
            reservation_date=payload.reservation_date,
            reservation_time=payload.reservation_time,
            day_of_week=day_of_week,
            guest_count=payload.guest_count,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Double booking: the selected table is already booked for that date and time",
        )

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Booking not found")

    if payload.status is not None:
        try:
            status_value = BookingStatus(payload.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid status value",
            )
        updated = update_booking_status(db, booking_id, status_value)
    return updated

# DELETE
    # Cancels a booking
@router.delete("/{booking_id}", status_code = status.HTTP_200_OK)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    success = cancel_booking(db, booking_id)
    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Booking cannot be cancelled",
        )
    return {"message": "Booking cancelled successfully"}
