# CLIENT MODEL
# This file defines how clients are represented in the database

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base

# I'm gonna map the Client class to avoid errors with CRUD operations

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(BigInteger, primary_key = True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable = False)
    phone: Mapped[str] = mapped_column(String(30), nullable = False)
    email: Mapped[str] = mapped_column(String(254), nullable = False, unique=True)


