from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Pydantic v1")


class Note(BaseModel):
    title: str
    priority: Optional[int]
    body: Optional[str] = None


@app.post("/notes", response_model=Note, status_code=201)
def create_note(note: Note):
    return note


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int, q: Optional[int] = None):
    return Note(title="n", priority=None)
