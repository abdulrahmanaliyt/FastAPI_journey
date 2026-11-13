from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.student import Student


def get_all_students(db: Session, skip: int = 0, limit: int = 10):
    statement = (
        select(Student)
        .offset(skip)
        .limit(limit)
    )

    students = db.scalars(statement).all()

    return students

def create_student(db: Session, name: str):
    student = Student(name=name)

    db.add(student)

    try:
        db.commit()
        db.refresh(student)

    except IntegrityError:
        db.rollback()
        raise ValueError("Database constraint violation")

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
