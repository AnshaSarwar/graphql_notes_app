import strawberry
from typing import List, Optional
from enum import Enum

@strawberry.enum
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

@strawberry.type
class UserType:
    id: strawberry.ID
    email: str
    username: str
    role: UserRole

    @strawberry.field
    def notes(self, info) -> List["NoteType"]:
        from models.note import Note
        db = info.context.db
        return db.query(Note).filter(Note.owner_id == self.id).all()

@strawberry.type
class NoteType:
    id: strawberry.ID
    title: str
    content: str
    owner_id: int

    @strawberry.field
    def owner(self, info) -> UserType:
        from models.user import User
        db = info.context.db
        return db.query(User).filter(User.id == self.owner_id).first()

@strawberry.type
class TokenType:
    access_token: str
    token_type: str
