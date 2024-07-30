from datetime import datetime, timedelta

from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.app.auth.models import User, Profile
from src.app.auth.schemas import ProfileBase, UserCreate
from src.config import get_settings
from src.utils.database import get_db

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/login", scheme_name="JWT")

settings = get_settings()
secret_salt = settings.SECRET_SALT
algo = settings.ALGORITHM
access_token_expiry_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
refresh_token_expiry_minutes = settings.REFRESH_TOKEN_EXP_MINUTES
refresh_token_salt = settings.REFRESH_SECRET_SALT


async def create_access_token(user):

    expires = datetime.utcnow() + timedelta(minutes=int(access_token_expiry_minutes))
    encode = {'email': user.email, 'id': user.id, 'expires': expires}
    return jwt.encode(encode, secret_salt, algorithm=algo)


async def create_refresh_token(user) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=refresh_token_expiry_minutes)

    to_encode = {'email': user.email, 'id': user.id, 'expires': expires_delta}
    encoded_jwt = jwt.encode(to_encode, refresh_token_salt, algo)
    return encoded_jwt


async def user_already_exists(email, db: Session):
    db_user = db.query(User).filter(User.email == email).first()
    return db_user


async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email.lower().strip(),
        name=user.name.lower().strip(),
        hashed_password=bcrypt_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def create_user_profile(db: Session, profile: ProfileBase, user: UserCreate):
    db_profile = Profile(
        gender=profile.gender,
        age=profile.age,
        weight=profile.weight,
        height=profile.height,
        goal=profile.goal,
        physical_activity_level=profile.physical_activity_level,
        user_id=user.id
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


async def get_hashed_password(password: str):
    return bcrypt_context.hash(password)


async def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt_context.verify(password, hashed_pass)


async def authentication(form_data, db: Session):
    db_user = await user_already_exists(form_data.username, db)
    if not db_user:
        return None, "User doesnt exists"
    is_verified = await verify_password(form_data.password, db_user.hashed_password)
    if not is_verified:
        return None, "Password didn't match"
    return db_user, "User found"


