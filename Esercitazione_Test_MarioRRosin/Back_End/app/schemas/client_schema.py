# CLIENT SCHEMA
# This one defines how clients are represented in Pydantic models for data validation and serialization

from pydantic import BaseModel, EmailStr
from typing import Optional


# Base
class ClientBase(BaseModel):
    name: str
    phone: str
    email: EmailStr

# CREATE
class ClientCreate(ClientBase):
    pass

# READ
class ClientRead(ClientBase):
    id: int

    class Config:
        from_attributes = True

# UPDATE
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
