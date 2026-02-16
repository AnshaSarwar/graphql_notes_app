# GraphQL Context: Provides DB session and authentication for every request
from strawberry.fastapi import BaseContext
from sqlalchemy.orm import Session
from db.database import SessionLocal
from typing import Optional
from models.user import User
from core.security import verify_token

class Context(BaseContext):
    """Custom GraphQL context with database and authentication support."""
    
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self._current_user: Optional[User] = None  # Cache authenticated user

    async def get_current_user(self) -> Optional[User]:
        """Extract and verify JWT token, return authenticated User or None."""
        
        # Return cached user if already authenticated
        if self._current_user:
            return self._current_user

        # Extract Authorization header
        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        # Parse and verify JWT token
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            user_id = payload.get("id")
            if user_id:

                # Fetch user from database and cache
                user = self.db.query(User).filter(User.id == user_id).first()
                self._current_user = user
                return user
        except Exception:
            return None
        return None

async def get_context() -> Context:
    """Factory function: Creates a new Context with DB session for each request."""
    db = SessionLocal()
    return Context(db=db)
