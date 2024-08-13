from typing import Optional

from pydantic import BaseModel

from src.utils.enums import ExerciseCategoryEnum, PhysicalLevelEnum, WorkoutPlanType


class WorkoutPlanBase(BaseModel):
    workout_title: str
    sub_heading: str
    exercise_exp_level: PhysicalLevelEnum
    plan_type: Optional[WorkoutPlanType] = None
    total_workout_count: int
    total_time: int
    description: str
    calories_burn: int
    coach_id: Optional[int] = None


class WorkoutBase(BaseModel):
    name: str
    target_muscle: ExerciseCategoryEnum
    total_time: int
    description: str
    calories_burn: int
    workout_plan_id: int

    class Config:
        from_attributes = True


class WorkoutUpdate(BaseModel):
    name: Optional[str] = None
    target_muscle: Optional[ExerciseCategoryEnum] = None
    total_time: Optional[int] = None
    description: Optional[str] = None
    calories_burn: Optional[int] = None
    is_active: Optional[bool] = None
    workout_plan_id: Optional[int] = None