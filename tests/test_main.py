import os
import tempfile
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from notes_api.main import app
from notes_api.database import create_db_and_tables, get_session
from notes_api.models import Note


# create an in-memory SQLite database for testing
test_sqlite_url = "sqlite:///./test.db"
test_engine = create_engine(test_sqlite_url, connect_args={"check_same_thread": False})


def override_get_session():
    with Session(test_engine) as session:
        yield session


# override the dependency
app.dependency_overrides[get_session] = override_get_session


def setup_test_db():
    SQLModel.metadata.create_all(test_engine)


def teardown_test_db():
    SQLModel.metadata.drop_all(test_engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_note():
    # ensure tables exist
    setup_test_db()
    try:
        response = client.post(
            "/notes/",
            json={"title": "Test", "body": "Test body"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test"
        assert data["body"] == "Test body"
        assert "id" in data
        note_id = data["id"]

        # read it back
        response = client.get(f"/notes/{note_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test"

        # delete
        response = client.delete(f"/notes/{note_id}")
        assert response.status_code == 200
        assert response.json() == {"ok": True}
    finally:
        teardown_test_db()
