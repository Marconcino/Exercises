# Database connection setup using SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This has the task to connect to the database created on MySQL
# Make sure to replace the user, password, host, port, and database name as needed
DATABASE_URL = (
    "postgresql+psycopg2://postgres:root@localhost:5432/medical_clinic_db"
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
