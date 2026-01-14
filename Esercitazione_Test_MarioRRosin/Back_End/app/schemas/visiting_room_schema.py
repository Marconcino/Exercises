# Visiting Room schemas

from pydantic import BaseModel


# Base
class VisitRoomBase(BaseModel):
    room_number: str
    equipment: str | None = None


# CREATE
class VisitRoomCreate(VisitRoomBase):
    pass


# UPDATE
class VisitRoomUpdate(BaseModel):
    room_number: str | None = None
    equipment: str | None = None


# READ
class VisitRoomRead(VisitRoomBase):
    id: int

    class Config:
        from_attributes = True