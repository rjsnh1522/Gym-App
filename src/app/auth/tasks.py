from sqlalchemy.orm import Session

from src.app.auth.models import Profile


def update_profile_task(db: Session, user_id: int, is_coach: bool):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        if profile.is_coach != is_coach:
            profile.is_coach = is_coach
            db.commit()