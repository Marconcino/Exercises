from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    first_name: Mapped[str] = mapped_column(String(100), nullable = False)
    last_name: Mapped[str] = mapped_column(String(100), nullable = False)
    birth_date: Mapped[str] = mapped_column(String(10), nullable = False)
    email: Mapped[str] = mapped_column(String(150), unique = True, nullable = False)
    phone_number: Mapped[str] = mapped_column(String(20), unique = True, nullable = False)

    emergency_contact_name: Mapped[str] = mapped_column(String(100), nullable = True)
    emergency_contact_phone: Mapped[str] = mapped_column(String(20), nullable = True)