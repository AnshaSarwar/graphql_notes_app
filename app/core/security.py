import os
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import settings

# Modern hashing approach using pwdlib
password_hash = PasswordHash.recommended()

# Prevent timing attacks by hashing a dummy password for non-existent users
DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Hashes a plain-text password
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

# Verifies a plain-text password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception:
        return False

def authenticate_user(db_user, password: str):
    if not db_user:
        # Run verification against dummy hash to match response time
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user

# Generates a short-lived access token for authentication
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Standard JWT 'sub' claim for user identification
    if "sub" not in to_encode:
        if "username" in to_encode:
            to_encode["sub"] = to_encode["username"]
        elif "email" in to_encode:
            to_encode["sub"] = to_encode["email"]
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Decodes and validates a JWT token
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
