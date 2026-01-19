# TABLE MODEL
# This file defines how many tables are represented in the database.

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer
from app.database.db import Base

# I've mapped the Table class to avoid errors with CRUD operations
class Table(Base):
    __tablename__ = "tables"
    id: Mapped[int] = mapped_column(BigInteger, primary_key = True, autoincrement = True, index = True)
    table_number: Mapped[int] = mapped_column(Integer, nullable = False, unique = True)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable = False)


