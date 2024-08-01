from typing import Optional, List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.app.auth.models import User
from src.app.workout.models import WorkoutPlan
from src.app.workout.schemas import WorkoutPlanBase
from src.app.workout.services import create_workout_plan, workout_plan_already_exists
from src.utils.database import get_db
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/workout", tags=["workout"])


@router.get("/workout_plans", response_model=List[WorkoutPlanBase])
async def get_all_workouts(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user),
                           coach_id: Optional[int] = None):

    return db.query(WorkoutPlan).all()


@router.post("/workout_plans", status_code=status.HTTP_201_CREATED)
async def create_workout(workout: WorkoutPlanBase, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    already_exists = await workout_plan_already_exists(db, workout)
    if already_exists:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workout plan with same name already exists"
        )
    db_workout = await create_workout_plan(db, workout)
    return db_workout