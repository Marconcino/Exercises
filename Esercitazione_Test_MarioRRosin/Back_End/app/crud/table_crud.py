# TABLE CRUD
# This CRUD module provides functions to create, read, update, and delete Table records in the database

from sqlalchemy.orm import Session
from app.models.table import Table

# CREATE
def create_table(db: Session, table_number: int, max_capacity: int) -> Table:
    table = Table(table_number = table_number, max_capacity = max_capacity)

    db.add(table)
    db.commit()
    db.refresh(table)
    return table


# READ
# Get table by ID
def get_table(db: Session, table_id: int) -> Table | None:
    return db.query(Table).filter(Table.id == table_id).first()
# Get all tables
def get_tables(db: Session) -> list[Table]:
    return db.query(Table).all()
# Get table by table_number
def get_table_by_number(db: Session, table_number: int) -> Table | None:
    return db.query(Table).filter(Table.table_number == table_number).first()
# Get tables by minimum capacity
def get_tables_by_min_capacity(db: Session, min_capacity: int) -> list[Table]:
    return db.query(Table).filter(Table.max_capacity >= min_capacity).all()


# UPDATE
def update_table(
    db: Session,
    table_id: int,
    table_number: int | None = None,
    max_capacity: int | None = None
) -> Table | None:
    table = get_table(db, table_id)
    if not table:
        return None

    if table_number is not None:
        table.table_number = table_number
    if max_capacity is not None:
        table.max_capacity = max_capacity

    db.commit()
    db.refresh(table)
    return table


# DELETE
def delete_table(db: Session, table_id: int) -> bool:
    table = get_table(db, table_id)
    if not table:
        return False

    db.delete(table)
    db.commit()
    return True
