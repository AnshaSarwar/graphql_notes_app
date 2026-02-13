# Pydantic schemas for Note-related data validation and serialization
from pydantic import BaseModel
from .base import BaseSchema

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class NoteResponse(BaseSchema):
    id: int
    title: str
    content: str
    owner_id: int