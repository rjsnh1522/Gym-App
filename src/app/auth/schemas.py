from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from src.app.auth.models import User
from src.utils.enums import GenderEnum, GoalEnum, PhysicalLevelEnum, ProfileType


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    email_verified: bool

    class Config:
        orm_mode = True
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProfileBase(BaseModel):
    gender: Optional[GenderEnum]
    age: Optional[int]
    weight: Optional[int]
    height: Optional[int]
    goal: Optional[GoalEnum]
    profile_type: Optional[ProfileType]
    physical_activity_level: Optional[PhysicalLevelEnum]


class UserSignup(BaseModel):
    user: UserCreate
    profile: ProfileBase


class CoachBase(BaseModel):
    experience: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class CoachOut(BaseModel):
    id: int
    experience: int
    user: UserOut
    profile: Optional[ProfileBase]
