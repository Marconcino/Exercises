from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database.db import get_db
from app.schemas.table_schema import (TableCreate, TableUpdate, TableRead as TableResponse)
from app.crud.table_crud import (create_table, get_table, get_tables, update_table, delete_table)

router = APIRouter(
    prefix = "/tables",
    tags = ["Tables"],
)

# GET Every Table
@router.get("/", response_model = List[TableResponse])
def read_tables(db: Session = Depends(get_db)):
    return get_tables(db)

# GET Table by id
@router.get("/{table_id}", response_model = TableResponse)
def read_table(table_id: int, db: Session = Depends(get_db)):
    table = get_table(db, table_id)
    if not table:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Table not found")
    return table


# POST
# Creates a new Table
@router.post("/", response_model = TableResponse, status_code = status.HTTP_201_CREATED)
def create_new_table(payload: TableCreate, db: Session = Depends(get_db)):
    try:
        return create_table(db, payload.table_number, payload.max_capacity)
    except IntegrityError:
        db.rollback()
        # table_number is UNIQUE
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Table number already exists",
        )


# PUT
# Update an existing Table
@router.put("/{table_id}", response_model = TableResponse)
def modify_table(table_id: int, payload: TableUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_table(db, table_id, payload.table_number, payload.max_capacity)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Table number already exists",
        )
    if not updated:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Table not found")
    return updated


# DELETE
@router.delete("/{table_id}", status_code = status.HTTP_200_OK)
def remove_table(table_id: int, db: Session = Depends(get_db)):
    success = delete_table(db, table_id)
    if not success:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Table not found")
    return {"message": "Table deleted successfully"}
