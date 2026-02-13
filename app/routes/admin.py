from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from db.crud_utils import db_delete
from models.user import User
from schemas.user import UserResponse, UserRole
from dependencies.auth import get_current_admin_user


# Admin router for admin-specific operations
router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse], dependencies=[Depends(get_current_admin_user)])
def read_all_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == UserRole.USER).all()

@router.delete("/users/{user_id}", dependencies=[Depends(get_current_admin_user)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_delete(db, user, "Database error occurred during user deletion")
    return {"detail": f"User {user_id} hard deleted by admin"}
