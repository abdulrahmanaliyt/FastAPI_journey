from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_all_users(db: Session):
    statement = select(User)

    return db.scalars(statement).all()