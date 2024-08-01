from sqlalchemy.orm import Session

from src.app.workout.models import WorkoutPlan
from src.app.workout.schemas import WorkoutPlanBase
from src.utils.enums import WorkoutPlanType


async def workout_plan_already_exists(db: Session, workout: WorkoutPlanBase):
    return db.query(WorkoutPlan).filter(WorkoutPlan.workout_title == workout.workout_title).first()


async def create_workout_plan(db: Session, workout: WorkoutPlanBase):
    db_workout = WorkoutPlan(
        workout_title=workout.workout_title,
        sub_heading=workout.sub_heading,
        exercise_exp_level=workout.exercise_exp_level,
        plan_type=workout.plan_type if workout.plan_type else WorkoutPlanType.DEFAULT,
        total_workout_count=workout.total_workout_count,
        total_time=workout.total_time,
        description=workout.description,
        calories_burn=workout.calories_burn,
        coach_id=workout.coach_id if workout.coach_id else None
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout
