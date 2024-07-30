from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from src.utils.database import Base
from src.utils.enums import GenderEnum, GoalEnum, PhysicalLevelEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    #relationship
    profile = relationship("Profile", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    gender = Column(Enum(GenderEnum), default=GenderEnum.MALE)
    age = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    goal = Column(Enum(GoalEnum), nullable=False)
    physical_activity_level = Column(Enum(PhysicalLevelEnum), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="profile")
    created_at = Column(DateTime, default=datetime.now())


class Verification(Base):
    __tablename__ = "verifications"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    verification_code = Column(String)
    expiry = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())
    verified_on = Column(DateTime, default=datetime.now())