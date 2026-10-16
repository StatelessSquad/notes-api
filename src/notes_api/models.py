from sqlmodel import Field, SQLModel
from datetime import datetime


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
