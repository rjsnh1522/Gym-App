from fastapi import APIRouter

from src.app.auth.views import router as auth_router


routers = APIRouter(prefix="/v1")

routers.include_router(auth_router)