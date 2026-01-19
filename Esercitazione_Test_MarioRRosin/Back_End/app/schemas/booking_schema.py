# BOOKING SCHEMA
# This one defines how bookings are represented in Pydantic models for data validation and serialization

from pydantic import BaseModel
from datetime import date, time as dt_time
from typing import Optional


class BookingBase(BaseModel):
    client_id: int
    table_id: int
    reservation_date: date
    reservation_time: dt_time
    guest_count: int


class BookingCreate(BookingBase):
    # optional: allow setting status explicitly, otherwise default pending
    status: Optional[str] = None


class BookingRead(BookingBase):
    id: int
    day_of_week: str
    status: str

    class Config:
        from_attributes = True


class BookingUpdate(BaseModel):
    client_id: Optional[int] = None
    table_id: Optional[int] = None
    reservation_date: Optional[date] = None
    reservation_time: Optional[dt_time] = None
    guest_count: Optional[int] = None
    status: Optional[str] = None
    
