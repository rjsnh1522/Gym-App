from typing import Optional, List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.app.auth.models import User
from src.app.auth.services import save_workouts, get_workout_by_id
from src.app.workout.models import WorkoutPlan
from src.app.workout.schemas import WorkoutPlanBase, WorkoutBase, WorkoutUpdate
from src.app.workout.services import create_workout_plan, workout_plan_already_exists
from src.utils.database import get_db
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/workout", tags=["workout"])


@router.get("/workout_plans", response_model=List[WorkoutPlanBase])
async def get_all_workout_plans(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user),
                           coach_id: Optional[int] = None):
    all_workout_plans = db.query(WorkoutPlan)
    if coach_id:
        all_workout_plans = all_workout_plans.filter(WorkoutPlan.coach_id == coach_id)

    return all_workout_plans.all()


@router.post("/workout_plans", status_code=status.HTTP_201_CREATED)
async def create_workout_plans(workout_plan: WorkoutPlanBase, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    already_exists = await workout_plan_already_exists(db, workout_plan)
    if already_exists:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workout plan with same name already exists"
        )
    db_workout = await create_workout_plan(db, workout_plan)
    return db_workout


@router.post("/workouts", status_code=status.HTTP_201_CREATED)
async def create_workouts(workout: WorkoutBase, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):

    workout = await save_workouts(db, workout)
    if not workout:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request"
        )
    return workout

@router.patch("/workouts/{workout_id}/", status_code=status.HTTP_200_OK)
async def create_workouts(workout_id: int, db: Session = Depends(get_db),
                          workout_update: WorkoutUpdate = None,
                          current_user: User = Depends(get_current_user)):

    if not workout_id:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request"
        )

    db_workout, mes = await get_workout_by_id(db=db, workout_id=workout_id)
    if not db_workout:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bad request"
        )

    update_data = workout_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_workout, key, value)
    db.commit()
    db.refresh(db_workout)
    return db_workout

