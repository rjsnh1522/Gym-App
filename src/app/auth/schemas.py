from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from src.utils.enums import GenderEnum, GoalEnum, PhysicalLevelEnum


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class ProfileBase(BaseModel):
    gender: Optional[GenderEnum]
    age: Optional[int]
    weight: Optional[int]
    height: Optional[int]
    goal: Optional[GoalEnum]
    physical_activity_level: Optional[PhysicalLevelEnum]


class UserSignup(BaseModel):
    user: UserCreate
    profile: ProfileBase

