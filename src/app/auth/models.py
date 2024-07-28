from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from src.utils.database import Base
from src.utils.enums import GenderEnum, GoalEnum, PhysicalLevelEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    #relationship
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="users")


class Profile(Base):
    __tablename__ = 'profiles'
    gender = Column(Enum(GenderEnum), default=GenderEnum.MALE)
    age = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    Goal = Column(Enum(GoalEnum), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    physical_activity_level = Column(Enum(PhysicalLevelEnum), nullable=False)

    user = relationship("User", back_populates="profiles")
