# CLIENT CRUD
# This CRUD module provides functions to create, read, update, and delete Client records in the database
from sqlalchemy.orm import Session
from app.models.client import Client

# CREATE
def create_client(db: Session, name: str, phone: str, email: str) -> Client:
    client = Client(name = name, phone = phone, email = email)

    db.add(client)
    db.commit()
    db.refresh(client)
    return client

# READ
# Get all clients
def get_clients(db: Session) -> list[Client]:
    return db.query(Client).all()
# Get client by ID
def get_client(db: Session, client_id: int) -> Client | None:
    return db.query(Client).filter(Client.id == client_id).first()
# Get client by email
def get_client_by_email(db: Session, email: str) -> Client | None:
    return db.query(Client).filter(Client.email == email).first()


# UPDATE
def update_client(
    db: Session,
    client_id: int,
    name: str | None = None,
    phone: str | None = None,
    email: str | None = None
) -> Client | None:
    client = get_client(db, client_id)
    if not client:
        return None

    if name is not None:
        client.name = name
    if phone is not None:
        client.phone = phone
    if email is not None:
        client.email = email

    db.commit()
    db.refresh(client)
    return client


# DELETE (hard delete)
def delete_client(db: Session, client_id: int) -> bool:
    client = get_client(db, client_id)
    if not client:
        return False

    db.delete(client)
    db.commit()
    return True
