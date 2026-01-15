from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.db import SessionLocal
from app.schemas.visiting_room_schema import VisitingRoomCreate, VisitRoomRead as VisitingRoomResponse
from app.crud.visiting_room_crud import (
    create_visiting_room,
    get_visiting_rooms,
    get_visiting_room,
)

router = APIRouter(
    prefix = "/visiting-rooms",
    tags = ["Visiting Rooms"]
)


@router.post("/", response_model = VisitingRoomResponse)
def create_room(
    room: VisitingRoomCreate,
    db: Session = Depends(SessionLocal)
):
    """
    Create a visiting room.
    """
    return create_visiting_room(db, room)


# Retrieve all visiting rooms
@router.get("/", response_model=List[VisitingRoomResponse])
def read_all_rooms(db: Session = Depends(SessionLocal)):
    return get_visiting_rooms(db)


# Retrieve a visiting room by ID
@router.get("/{room_id}", response_model=VisitingRoomResponse)
def read_room(room_id: int, db: Session = Depends(SessionLocal)):
    room = get_visiting_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Visiting room not found")
    return room
