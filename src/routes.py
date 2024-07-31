from fastapi import APIRouter

from src.app.auth.views import router as auth_router
from src.app.workout.views import router as workout_router


routers = APIRouter(prefix="/v1")

routers.include_router(auth_router)
routers.include_router(workout_router)