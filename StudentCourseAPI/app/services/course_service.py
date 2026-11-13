from builtins import int

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course import Course


# Get all courses
def get_all_courses(db: Session):
    statement = select(Course)

    courses = db.scalars(statement).all()

    return courses


# Create a new courses
def create_course(db: Session, course_data):
    course = Course(
        title=course_data.title,
        duration=course_data.duration,
        price=course_data.price,
        description=course_data.description
    )    
    db.add(course)
    db.commit()
    db.refresh(course)

    return course


# Update Courses partially
def update_course(db: Session, course_id: int, course_data):
    statement = select(Course).where(Course.id == course_id)
    course = db.scalars(statement).first()

    if not course:
        return None

    update_data = course_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(course, field, value)

    try:
        db.commit()
        db.refresh(course)
    except Exception:
        db.rollback()
        raise

    return course


# Replacement service function

def replace_course(db: Session, course_id: int, course_data):
    statement = select(Course).where(Course.id == course_id)
    course = db.scalars(statement).first()

    if not course:
        return None

    course.title = course_data.title
    course.duration = course_data.duration
    course.price = course_data.price
    course.description = course_data.description

    try:
        db.commit()
        db.refresh(course)
    except Exception:
        db.rollback()
        raise

    return course


def delete_course(db: Session, course_id: int):
    statement = select(Course).where(Course.id == course_id)
    course = db.scalars(statement).first()

    if course:
        db.delete(course)
        db.commit()
        return True

    return False