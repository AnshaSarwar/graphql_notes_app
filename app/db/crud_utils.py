from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# Saves a single object to the database with transaction safety.
def db_save(db: Session, obj: any, error_detail: str = "Database error occurred"):
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )

# Commits the current session with transaction safety. Useful for updates.
def db_commit(db: Session, error_detail: str = "Database error occurred"):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )

def db_delete(db: Session, obj: any, error_detail: str = "Database error occurred"):
    """
    Deletes an object from the database with transaction safety.
    """
    try:
        db.delete(obj)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )
