# With base.py we define the base class for our ORM
# That allows us to create models

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass