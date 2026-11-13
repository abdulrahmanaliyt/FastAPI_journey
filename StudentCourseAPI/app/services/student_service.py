from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.student import Student


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student


def get_all_students(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    name: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc"
):
    statement = select(Student)

    if search:
        statement = statement.where(
            Student.name.ilike(f"%{search}%")
        )

    if name:
        statement = statement.where(
            Student.name.ilike(name)
        )

    sort_column = {
        "id": Student.id,
        "name": Student.name
    }[sort_by]

    if sort_order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    statement = statement.offset(skip).limit(limit)

    return db.scalars(statement).all()

def create_student(db: Session, name: str):
    student = Student(name=name)

    try:
        db.add(student)
        db.commit()
        db.refresh(student)

    except IntegrityError as error:
        db.rollback()
        raise ValueError("Database constraint violation") from error

    except Exception:
        db.rollback()
        raise

    return student

def get_student_by_id(db: Session, student_id: int, user_id: int):
    statement = select(Student).where(
        Student.id == student_id,
        Student.user_id == user_id
    )

    student = db.scalars(statement).first()

    return student


class StudentProfileAlreadyExists(Exception):
    pass


class StudentProfileNotFound(Exception):
    pass


def create_my_student_profile(
    db: Session,
    user_id: int,
    name: str
):
    # Check whether this user already has a profile
    existing_student = db.scalar(
        select(Student).where(Student.user_id == user_id)
    )

    if existing_student:
        raise StudentProfileAlreadyExists(
            "You already have a student profile"
        )

    student = Student(
        name=name,
        user_id=user_id
    )

    db.add(student)

    try:
        db.commit()
        db.refresh(student)
    except Exception:
        db.rollback()
        raise

    return student


def get_my_student_profile(
    db: Session,
    user_id: int
):
    student = db.scalar(
        select(Student).where(Student.user_id == user_id)
    )

    if not student:
        raise StudentProfileNotFound(
            "Student profile not found. Please create your profile first."
        )

    return student
