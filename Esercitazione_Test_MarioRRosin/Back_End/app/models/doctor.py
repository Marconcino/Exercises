from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    first_name: Mapped[str] = mapped_column(String(100), nullable = False)
    last_name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[str] = mapped_column(String(150), unique = True, nullable = False)
    phone_number: Mapped[str] = mapped_column(String(20), unique = True, nullable = False)
    specialization: Mapped[str] = mapped_column(String(100), nullable = False)

    # Availability stored as JSON/text (can be refined later)
    availability: Mapped[str] = mapped_column(Text, nullable = False)