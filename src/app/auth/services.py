import uuid
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import MessageSchema, FastMail
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.app.auth.models import User, Profile, Verification
from src.app.auth.schemas import ProfileBase, UserCreate
from src.config import get_settings
from src.utils.database import get_db
from src.utils.email_api import conf

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/login", scheme_name="JWT")

settings = get_settings()
secret_salt = settings.SECRET_SALT
algo = settings.ALGORITHM
access_token_expiry_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
refresh_token_expiry_minutes = settings.REFRESH_TOKEN_EXP_MINUTES
refresh_token_salt = settings.REFRESH_SECRET_SALT
base_url = settings.BASE_URL


async def create_access_token(user):

    expires = datetime.utcnow() + timedelta(minutes=int(access_token_expiry_minutes))
    encode = {'email': user.email, 'id': user.id, 'expires': str(expires)}
    return jwt.encode(encode, secret_salt, algorithm=algo)


async def create_refresh_token(user) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=refresh_token_expiry_minutes)

    to_encode = {'email': user.email, 'id': user.id, 'expires': str(expires_delta)}
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


async def create_verification_record(user, db: Session, verification_code: str):
    verification = Verification(
        verification_code=verification_code,
        user_id=user.id
    )
    db.add(verification)
    db.commit()
    return verification


async def send_verification_email(user_id: int, db):
    token = f"{str(uuid.uuid4())}{str(uuid.uuid4())}"
    verification_link = f"{base_url}/verify-email?token={token}"
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        verification = await create_verification_record(user, db, verification_code=token)
        message = MessageSchema(
            subject="Email Verification",
            recipients=[user.email],
            body=f"Click the link to verify your email: {verification_link}",
            subtype="html"
        )
        if settings.ENABLE_EMAIL:
            fm = FastMail(conf)
            await fm.send_message(message)
    else:
        print(f"User not found with user_id {user_id}")
