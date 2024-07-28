from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.auth.schemas import UserCreate
from src.app.auth.services import user_already_exists
from src.utils.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED, name="signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await user_already_exists(db, user)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this email, please log in"
        )
    db_user = await create_user_svc(db, user)