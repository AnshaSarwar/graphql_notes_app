import strawberry
from strawberry.fastapi import BaseContext
from sqlalchemy.orm import Session
from db.database import SessionLocal
from typing import Optional
from models.user import User
from core.security import verify_token

class Context(BaseContext):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self._current_user: Optional[User] = None

    async def get_current_user(self) -> Optional[User]:
        if self._current_user:
            return self._current_user

        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            user_id = payload.get("id")
            if user_id:
                user = self.db.query(User).filter(User.id == user_id).first()
                self._current_user = user
                return user
        except Exception:
            return None
        return None

async def get_context() -> Context:
    db = SessionLocal()
    try:
        return Context(db=db)
    finally:
        # Note: We keep the session open for the context
        # Strawberry will handle the cleanup if we wrap it properly or 
        # we can close it in a custom logic. 
        # Actually, for Strawberry Context, it's better to manage session lifecycle.
        pass
