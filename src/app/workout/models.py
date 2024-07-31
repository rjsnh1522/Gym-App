from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import validates, relationship

from src.utils.database import Base
from src.utils.enums import PhysicalLevelEnum, ExerciseCategoryEnum, WorkoutPlanType


class WorkoutPlan(Base):
    __tablename__ = "workoutplans"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    workout_title = Column(String, unique=True, index=True, nullable=False)
    sub_heading = Column(String, index=True, nullable=False)
    exercise_exp_level = Column(Enum(PhysicalLevelEnum), nullable=False)
    plan_type = Column(Enum(WorkoutPlanType), nullable=False, default=WorkoutPlanType.DEFAULT)
    total_workout_count = Column(Integer)
    total_time = Column(Integer)
    Description = Column(LONGTEXT, default=False)
    calories_burn = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="workout_plans")

    created_at = Column(DateTime, default=datetime.now())

    @validates('total_workout_count')
    def validate_total_workout_count(self, key, value):
        assert value > 0
        return value

    @validates('calories_burn')
    def validate_calories_burn(self, key, value):
        assert value > 0
        return value


class Workouts(Base):
    __tablename__ = "workouts"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    target_muscle = Column(Enum(ExerciseCategoryEnum), nullable=False)
    total_time = Column(Integer)
    Description = Column(LONGTEXT, default=False)
    calories_burn = Column(Integer)

