from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.auth.models import User
from src.app.workout.models import WorkoutPlan
from src.app.workout.schemas import WorkoutPlanBase
from src.utils.database import get_db
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/workout", tags=["workout"])


@router.get("/workout_plans", response_model=List[WorkoutPlanBase])
async def get_all_workouts(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user),
                           coach_id: Optional[int] = None):

    return db.query(WorkoutPlan).all()


