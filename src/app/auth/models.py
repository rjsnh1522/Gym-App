from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from src.utils.database import Base
from src.utils.enums import GenderEnum, GoalEnum, PhysicalLevelEnum, ProfileType


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_coach = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    #relationship
    profile = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    coach = relationship("Coach", back_populates="user", uselist=False)


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    gender = Column(Enum(GenderEnum), default=GenderEnum.MALE)
    age = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    goal = Column(Enum(GoalEnum), nullable=False)
    physical_activity_level = Column(Enum(PhysicalLevelEnum), nullable=False, default=PhysicalLevelEnum.BEGINNER)
    profile_type = Column(Enum(ProfileType), default=ProfileType.TRAINEE)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="profile")
    workout_plans = relationship("WorkoutPlan", back_populates="user")

    created_at = Column(DateTime, default=datetime.now())


class Verification(Base):
    __tablename__ = "verifications"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    verification_code = Column(String)
    expiry = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())
    verified_on = Column(DateTime, default=datetime.now())


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="coach")
    review = relationship("Review", back_populates="coach")
    workout_plans = relationship("WorkoutPlan", back_populates="coach")
    experience = Column(Integer)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coaches.id", ondelete="CASCADE"), nullable=False)
    coach = relationship("Coach", back_populates="review")
    rating = Column(Integer)
    reviewer = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(String)