from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from db.crud_utils import db_save, db_commit, db_delete
from models.note import Note
from schemas.note import NoteCreate, NoteUpdate, NoteResponse
from schemas.user import UserResponse as UserSchemaResponse
from dependencies.auth import get_current_regular_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse)
def create_note(note_in: NoteCreate, current_user: UserSchemaResponse = Depends(get_current_regular_user), db: Session = Depends(get_db)):
    new_note = Note(
        title=note_in.title,
        content=note_in.content,
        owner_id=current_user.id
    )
    return db_save(db, new_note, "Database error occurred while creating note")

@router.get("/", response_model=List[NoteResponse])
def read_notes(current_user: UserSchemaResponse = Depends(get_current_regular_user), db: Session = Depends(get_db)):
    return db.query(Note).filter(Note.owner_id == current_user.id).all()

@router.get("/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, current_user: UserSchemaResponse = Depends(get_current_regular_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_in: NoteUpdate, current_user: UserSchemaResponse = Depends(get_current_regular_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    update_data = note_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
    
    db_commit(db, "Database error occurred while updating note")
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, current_user: UserSchemaResponse = Depends(get_current_regular_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_delete(db, note, "Database error occurred while deleting note")
    return {"detail": "Note deleted successfully"}
