from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.auth.models import User
from src.app.auth.schemas import UserCreate, UserOut, UserSignup
from src.app.auth.services import user_already_exists, create_user, create_user_profile
from src.utils.database import get_db
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED, name="signup")
async def signup(user_signup: UserSignup, db: Session = Depends(get_db)):
    db_user = await user_already_exists(db, user_signup.user)
    if db_user:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this email, please log in"
        )
    user = await create_user(db, user_signup.user)
    profile = await create_user_profile(db, user_signup.profile, user)
    return {"user": user, "profile": profile}

@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(me: User = Depends(get_current_user)):
    return me

