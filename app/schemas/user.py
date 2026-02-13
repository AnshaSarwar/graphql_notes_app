# Pydantic schemas for User-related data validation and serialization
from enum import Enum
from pydantic import BaseModel
from .base import BaseSchema

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    email: str
    username: str
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None
    role: UserRole | None = None
    password: str | None = None

class UserResponse(UserBase, BaseSchema):
    id: int