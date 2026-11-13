from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def register_user(db: Session, user_data: UserCreate):

    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="user"
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()
        raise EmailAlreadyRegisteredError(
            "Email already registered"
        )

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    statement = select(User).where(User.email == email)

    user = db.scalar(statement)

    if user is None:
        raise InvalidCredentialsError(
            "Incorrect email or password"
        )

    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError(
            "Incorrect email or password"
        )

    return user