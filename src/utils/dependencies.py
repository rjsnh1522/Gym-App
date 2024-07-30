from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.app.auth.models import User
from src.config import get_settings
from src.utils.database import get_db

settings = get_settings()
secret_salt = settings.SECRET_SALT
algo = settings.ALGORITHM

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/login", scheme_name="JWT")


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
    except Exception as e:
        print(f"Unexpected Error: {e}")  # Log unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )

