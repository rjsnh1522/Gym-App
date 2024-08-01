from sqlalchemy.orm import Session

from src.app.auth.models import Profile, User


def update_profile_task(db: Session, user_id: int, is_coach: bool):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_coach = is_coach
        db.commit()