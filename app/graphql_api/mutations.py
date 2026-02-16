import strawberry
from datetime import timedelta
from core.config import settings
from core.security import create_access_token, get_password_hash, authenticate_user
from db.crud_utils import db_save, db_delete
from models.user import User
from models.note import Note
from graphql_api.types import UserType, NoteType, TokenType, UserRole
from typing import Optional

@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(
        self, 
        info, 
        email: str, 
        username: str, 
        password: str, 
        role: UserRole = UserRole.USER
    ) -> UserType:
        db = info.context.db
        if db.query(User).filter((User.email == email) | (User.username == username)).first():
            raise Exception("User already registered")
        
        new_user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            role=role.value
        )
        return db_save(db, new_user)

    @strawberry.mutation
    def login(self, info, username: str, password: str) -> TokenType:
        db = info.context.db
        user = db.query(User).filter((User.email == username) | (User.username == username)).first()
        
        if not user or not authenticate_user(user, password):
            raise Exception("Invalid credentials")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "id": user.id, "email": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        return TokenType(access_token=access_token, token_type="bearer")

    @strawberry.mutation
    async def create_note(self, info, title: str, content: str) -> NoteType:
        user = await info.context.get_current_user()
        if not user:
            raise Exception("Not authenticated")
        
        db = info.context.db
        new_note = Note(title=title, content=content, owner_id=user.id)
        return db_save(db, new_note)

    @strawberry.mutation
    async def delete_note(self, info, id: int) -> bool:
        user = await info.context.get_current_user()
        if not user:
            raise Exception("Not authenticated")
        
        db = info.context.db
        note = db.query(Note).filter(Note.id == id, Note.owner_id == user.id).first()
        if not note:
            raise Exception("Note not found or access denied")
        
        db_delete(db, note)
        return True
