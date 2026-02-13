from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from db.database import get_db
from db.crud_utils import db_save
from models.user import User
from schemas.user import UserCreate, UserResponse
from schemas.token import Token
from core.security import create_access_token, get_password_hash, authenticate_user
from core.config import settings


# Authentication router for user registration and login
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user with same email OR username already exists
    if db.query(User).filter((User.email == user_in.email) | (User.username == user_in.username)).first():
        raise HTTPException(status_code=400, detail="User already registered")
    
    new_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )
    return db_save(db, new_user, "Database error occurred during registration")

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Supports both email and username as the login 'username' field
    user = db.query(User).filter((User.email == form_data.username) | (User.username == form_data.username)).first()
    
    if not authenticate_user(user, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "email": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
