from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class VisitingRoom(Base):
    __tablename__ = "visiting_rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    room_number: Mapped[str] = mapped_column(String(50), unique = True, nullable = False)
    floor: Mapped[int] = mapped_column(String(50), nullable = False)
    equipment: Mapped[str] = mapped_column(Text, nullable = True)