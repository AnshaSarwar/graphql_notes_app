import strawberry
from datetime import timedelta
from core.config import settings
from core.security import create_access_token, get_password_hash, authenticate_user
from db.crud_utils import db_save, db_delete
from models.user import User
from models.note import Note
from graphql_api.types import UserType, NoteType, TokenType, UserRole

# Helper functions for role validation
def require_user_role(user):
    """Ensure the current user has 'user' role."""
    if not user:
        raise Exception("Not authenticated")
    if user.role != "user":
        raise Exception("Only regular users can manage notes")
    return user

def require_admin_role(user):
    """Ensure the current user has 'admin' role."""
    if not user:
        raise Exception("Not authenticated")
    if user.role != "admin":
        raise Exception("Admin access required")
    return user

# Mutation class to handle all mutation operations
@strawberry.type
class Mutation:

    # Register a new user
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

    # Login user
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

    # Admin: Read all regular users (excludes admins)
    @strawberry.mutation
    async def read_users(self, info) -> list[UserType]:
        user = require_admin_role(await info.context.get_current_user())
        db = info.context.db
        # Only return regular users, not admins
        return db.query(User).filter(User.role == "user").all()

    # Admin: Delete any regular user (cannot delete admins)
    @strawberry.mutation
    async def delete_user(self, info, id: int) -> bool:
        user = require_admin_role(await info.context.get_current_user())
        db = info.context.db
        target_user = db.query(User).filter(User.id == id).first()
        if not target_user:
            raise Exception("User not found")
        
        # Prevent deleting admin accounts
        if target_user.role == "admin":
            raise Exception("Cannot delete admin users")
        
        db_delete(db, target_user)
        return True

    # Read all notes (users only)
    @strawberry.mutation
    async def read_notes(self, info) -> list[NoteType]:
        user = require_user_role(await info.context.get_current_user())
        db = info.context.db
        return db.query(Note).filter(Note.owner_id == user.id).all()

    # Create a new note (users only)
    @strawberry.mutation
    async def create_note(self, info, title: str, content: str) -> NoteType:
        user = require_user_role(await info.context.get_current_user())
        db = info.context.db
        new_note = Note(title=title, content=content, owner_id=user.id)
        return db_save(db, new_note)

    # Update a note (users only)
    @strawberry.mutation
    async def update_note(self, info, id: int, title: str | None = None, content: str | None = None) -> NoteType:
        user = require_user_role(await info.context.get_current_user())
        db = info.context.db
        note = db.query(Note).filter(Note.id == id, Note.owner_id == user.id).first()
        if not note:
            raise Exception("Note not found or access denied")

        if title:
            note.title = title
        if content:
            note.content = content

        db.commit()
        db.refresh(note)
        return note

    # Delete a note (users only)
    @strawberry.mutation
    async def delete_note(self, info, id: int) -> bool:
        user = require_user_role(await info.context.get_current_user())
        db = info.context.db
        note = db.query(Note).filter(Note.id == id, Note.owner_id == user.id).first()
        if not note:
            raise Exception("Note not found or access denied")
        
        db_delete(db, note)
        return True
