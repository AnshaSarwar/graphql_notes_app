# Get current user from JWT, role-based dependency.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from core.security import verify_token
from schemas.user import UserRole, UserResponse

# OAuth2 scheme for dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Extracts user data from the access token and validates it
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    payload = verify_token(token)
    user_id: int = payload.get("id")
    username: str = payload.get("sub")
    if user_id is None or username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
    return UserResponse(
        id=user_id, 
        username=username, 
        email=payload.get("email"), 
        role=payload.get("role")
    )

def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user

# Ensures the current user has the ADMIN role
def get_current_admin_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can access this resource")
    return current_user

def required_admin(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can access this resource")
    return current_user

# Ensures the current user has the USER role (NOT Admin)
def get_current_regular_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    if current_user.role != UserRole.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrators cannot manage notes")
    return current_user