from sqlalchemy.orm import Session
from app.models.visiting_room import VisitingRoom

# CREATE
def create_visiting_room(db: Session, room_number: str, floor: int, equipment: str | None = None) -> VisitingRoom:
    room = VisitingRoom(room_number = room_number, floor = floor, equipment = equipment)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


# READ
def get_visiting_room(db: Session, room_id: int) -> VisitingRoom | None:
    return db.query(VisitingRoom).filter(VisitingRoom.id == room_id).first()


def get_visiting_rooms(db: Session) -> list[VisitingRoom]:
    return db.query(VisitingRoom).all()

# UPDATE
def update_visiting_room(
    db: Session,
    room_id: int,
    room_number: str | None = None,
    floor: int | None = None,
    equipment: str | None = None
) -> VisitingRoom | None:
    room = get_visiting_room(db, room_id)
    if not room:
        return None

    if room_number is not None:
        room.room_number = room_number
    if floor is not None:
        room.floor = floor
    if equipment is not None:
        room.equipment = equipment

    db.commit()
    db.refresh(room)
    return room


# DELETE
def delete_visiting_room(db: Session, room_id: int) -> bool:
    room = get_visiting_room(db, room_id)
    if not room:
        return False

    db.delete(room)
    db.commit()
    return True