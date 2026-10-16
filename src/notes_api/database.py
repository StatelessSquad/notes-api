from sqlmodel import Session, create_engine, SQLModel
from .models import Note

# SQLite database file with connect_args needed for SQLite
sqlite_file_name = "notes.db"
engine = create_engine(
    f"sqlite:///{sqlite_file_name}", connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
