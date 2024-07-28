from fastapi import Depends, status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.app.auth.models import User
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from src.config import get_settings
from src.utils.database import get_db

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

settings = get_settings()
secret_salt = settings.secret_salt
algo = settings.ALGORITHM
token_expiry = settings.TOKEN_EXP


async def create_access_token(user):
    encode = {'email': user.email, 'id': user.id}
    expires = datetime.utcnow() + timedelta(seconds=int(token_expiry))
    encode.update({'expires': expires})
    return jwt.encode(encode, secret_salt, algorithm=algo)


async def user_already_exists(db, user):
    db_user = db.query(User).filter(User.email == user.email).first()
    return db_user


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_salt, algorithms=[algo])
        username: str = payload.get("email")
        id: str = payload.get("id")
        exp: datetime = payload.get("expires")
        if datetime.fromtimestamp(exp) < datetime.now():
            raise credentials_exception
        if username is None or id is None:
            raise credentials_exception
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise credentials_exception
        return user
    except JWTError as e:
        print(f"Error in {e}")
        raise credentials_exception


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def create_user(db, user):
    db_user = User(
        email=user.email.lower().strip(),
        username=user.username.lower().strip(),
        hashed_password=bcrypt_context.hash(user.password),
        dob=user.dob,
        gender=user.gender,
        bio=user.bio,
        location=user.bio,
        name=user.name,
        profile_pic=user.profile_pic
    )
    db.add(db_user)
    db.commit()
    return db_user


async def get_hashed_password(password: str):
    return bcrypt_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt_context.verify(password, hashed_pass)
