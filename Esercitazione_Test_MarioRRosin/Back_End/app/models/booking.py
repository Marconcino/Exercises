# BOOKING MODEL
# This file defines how bookings are represented in the database 

import enum
from sqlalchemy import (BigInteger, Date, Time, Integer, Enum as SAEnum, ForeignKey, TIMESTAMP, text)
from datetime import date, time, datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base

# Using Enums to represent days of the week and booking status. They cannot be modified 
# I'm gonna map the Booking class to avoid errors with CRUD operations

class DayOfWeek(enum.Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

class BookingStatus(enum.Enum):
    confirmed = "confirmed"
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key = True, autoincrement = True, index = True)

    client_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("clients.id", ondelete = "RESTRICT"),
        nullable = False,
        index = True,
    )
    table_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tables.id", ondelete = "RESTRICT"),
        nullable = False,
        index = True,
    )

# Using date and time to set the date and time of the reservation
    reservation_date: Mapped[date] = mapped_column(Date, nullable = False, index = True)
    reservation_time: Mapped[time] = mapped_column(Time, nullable = False, index = True)

    day_of_week: Mapped[DayOfWeek] = mapped_column(
        SAEnum(DayOfWeek, native_enum = False),
        nullable = False,
    )

    guest_count: Mapped[int] = mapped_column(Integer, nullable = False)

    status: Mapped[BookingStatus] = mapped_column(
        SAEnum(BookingStatus, native_enum = False),
        nullable = False,
        server_default = text("'pending'"),
    )

# Using datetime so that I'm able to map the creation of the table's booking
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable = False,
        server_default = text("CURRENT_TIMESTAMP"),
    )
