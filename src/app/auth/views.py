from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.auth.models import User
from src.app.auth.schemas import UserCreate, UserOut
from src.app.auth.services import user_already_exists, create_user
from src.utils.database import get_db
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED, name="signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await user_already_exists(db, user)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this email, please log in"
        )
    db_user = await create_user(db, user)
    return db_user

@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(me: User = Depends(get_current_user)):
    return me

