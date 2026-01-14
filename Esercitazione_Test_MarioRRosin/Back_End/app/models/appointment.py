from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    doctor_id: Mapped[int] = mapped_column(Integer, nullable = False)
    patient_id: Mapped[int] = mapped_column(Integer, nullable = False)
    appointment_date: Mapped[str] = mapped_column(String(20), nullable = False)
    reason: Mapped[str] = mapped_column(Text, nullable = True)
    status: Mapped[str] = mapped_column(String(50), nullable = False, default = "Scheduled")
    notes: Mapped[str] = mapped_column(Text, nullable = True)

# Mapping the columns to make the Appointment table in the database and not crush 