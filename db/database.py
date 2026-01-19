from sqlmodel import Session, create_engine, SQLModel
from sqlmodel import SQLModel



import os
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

database_url = os.getenv("DATABASE_URL", sqlite_url)

connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}
engine = create_engine(database_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


