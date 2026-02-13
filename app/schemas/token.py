# Pydantic schemas for Authentication tokens and JWT payload data
from .base import BaseSchema

class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenData(BaseSchema):
    email: str | None = None