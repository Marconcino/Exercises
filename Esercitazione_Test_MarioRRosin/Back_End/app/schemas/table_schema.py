# TABLE SCHEMA
# This one defines how tables are represented in Pydantic models for data validation and serialization

from pydantic import BaseModel
from typing import Optional

# Base
class TableBase(BaseModel):
    table_number: int
    max_capacity: int

# CREATE
class TableCreate(TableBase):
    pass

# READ
class TableRead(TableBase):
    id: int

    class Config:
        from_attributes = True

# UPDATE
class TableUpdate(BaseModel):
    table_number: Optional[int] = None
    max_capacity: Optional[int] = None
