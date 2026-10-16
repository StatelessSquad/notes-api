from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from .database import create_db_and_tables, get_session
from .models import Note
from typing import List, Optional

app = FastAPI(title="notes-api", version="0.1.0")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/notes/", response_model=Note)
def create_note(note: Note, session: Session = Depends(get_session)):
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.get("/notes/", response_model=List[Note])
def read_notes(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    notes = session.exec(select(Note).offset(offset).limit(limit)).all()
    return notes


@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.patch("/notes/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    session: Session = Depends(get_session),
):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if title is not None:
        note.title = title
    if body is not None:
        note.body = body
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"ok": True}
