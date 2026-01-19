from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database.db import get_db
from app.schemas.client_schema import (ClientCreate, ClientUpdate, ClientRead as ClientResponse)
from app.crud.client_crud import (create_client, get_client, get_clients, update_client, delete_client)

router = APIRouter(
    prefix = "/clients",
    tags = ["Clients"],
)


# GET (by id)
@router.get("/{client_id}", response_model=ClientResponse)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


# GET (list)
@router.get("/", response_model = List[ClientResponse])
def read_clients(db: Session = Depends(get_db)):
    return get_clients(db)


# POST
@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_new_client(payload: ClientCreate, db: Session = Depends(get_db)):
    try:
        return create_client(db, payload.name, payload.phone, payload.email)
    except IntegrityError:
        db.rollback()
        # The email is UNIQUE for every client
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email already exists",
        )


# PUT
@router.put("/{client_id}", response_model=ClientResponse)
def modify_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_client(db, client_id, payload.name, payload.phone, payload.email)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return updated


# DELETE
@router.delete("/{client_id}", status_code=status.HTTP_200_OK)
def remove_client(client_id: int, db: Session = Depends(get_db)):
    success = delete_client(db, client_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return {"message": "Client deleted successfully"}
