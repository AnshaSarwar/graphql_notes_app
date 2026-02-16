import strawberry
from typing import List, Optional
from graphql.types import UserType, NoteType, UserRole
from models.note import Note
from models.user import User

@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info) -> Optional[UserType]:
        user = await info.context.get_current_user()
        return user

    @strawberry.field
    async def my_notes(self, info) -> List[NoteType]:
        user = await info.context.get_current_user()
        if not user:
            raise Exception("Not authenticated")
        db = info.context.db
        return db.query(Note).filter(Note.owner_id == user.id).all()

    @strawberry.field
    async def admin_all_users(self, info) -> List[UserType]:
        user = await info.context.get_current_user()
        if not user or user.role != "admin":
            raise Exception("Forbidden")
        db = info.context.db
        return db.query(User).all()
