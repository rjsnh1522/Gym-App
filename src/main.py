from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db, Base, engine
from src.routes import routers

# Base.metadata.drop_all(bind=engine)

# Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="GYM APP",
    description="Gym app description",
    version="0.1")


app.include_router(routers)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}