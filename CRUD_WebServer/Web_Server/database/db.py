from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "postgrees"
PASSWORD = "SQLsql!!"
HOST = "localhost"
PORT = "5432"
DB_NAME = "api_project_db"

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)
Base = declarative_base()