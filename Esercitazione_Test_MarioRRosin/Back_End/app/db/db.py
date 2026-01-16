# Database connection setup using SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This has the task to connect to the database created on MySQL
# Make sure to replace the user, password, host, port, and database name as needed
DATABASE_URL = (
    "mysql+mysqlconnector://root:root@localhost:3306/medical_clinic"
)

engine = create_engine(
    DATABASE_URL,
    echo = True  # useful during development
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
