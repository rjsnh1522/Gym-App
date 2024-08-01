from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.auth.models import User
from src.app.auth.schemas import UserOut, UserSignup, CoachBase, CoachOut

from src.app.auth.services import (user_already_exists,
                                   create_user,
                                   create_user_profile,
                                   authentication,
                                   create_access_token,
                                   create_refresh_token,
                                   send_verification_email,
                                   create_coach_data,
                                   get_coach_data)
from src.app.auth.tasks import update_profile_task

from src.utils.database import get_db
from src.utils.dependencies import get_current_user
from src.utils.email_api import send_email_async, send_email_background

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED, name="signup")
async def signup(user_signup: UserSignup,
                 background_tasks: BackgroundTasks,
                 db: Session = Depends(get_db)):
    db_user = await user_already_exists(user_signup.user.email, db)
    if db_user:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this email, please log in"
        )
    user = await create_user(db, user_signup.user)
    profile = await create_user_profile(db, user_signup.profile, user)
    background_tasks.add_task(send_verification_email, user.id, db)
    return {"user": UserOut.from_orm(user), "profile": profile}


@router.get('/me', summary='Get details of currently logged in user')
async def profile(current_user: User = Depends(get_current_user)):
    user = current_user
    profile = user.profile
    return {"user": UserOut.from_orm(user), "profile": profile}


@router.post("/login", summary="Login user and give access token and refresh token",
             status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user, msg = await authentication(form_data, db)
    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg
        )
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get('/send-email/asynchronous')
async def send_email_asynchronous(current_user: User = Depends(get_current_user)):
    await send_email_async(
        subject='Hello World',
        email_to='test@gmail.com',
        body={'title': 'Hello World', 'name': 'John Doe'})
    return 'Success'


@router.get('/send-email/backgroundtasks')
def send_email_background_tasks(background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    send_email_background(
        background_tasks, subject='Hello World',
        email_to='test@gmail.com',
        body={'title': 'Hello World', 'name':'John Doe'})

    return 'Success'


@router.post('/coach', status_code=status.HTTP_201_CREATED)
async def create_coach(coach: CoachBase,
                       background_tasks: BackgroundTasks,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_coach = await get_coach_data(db, user_id=coach.user_id)
    if not db_coach:
        db_coach = await create_coach_data(db, coach)
    background_tasks.add_task(update_profile_task, db, db_coach.user_id, True)
    return db_coach


@router.get('/coach/{coach_id}', status_code=status.HTTP_201_CREATED, response_model=CoachOut)
async def create_coach(coach_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_coach = await get_coach_data(db, coach_id=coach_id)
    return db_coach
