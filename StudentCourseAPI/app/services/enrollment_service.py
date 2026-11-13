from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment


class StudentNotFoundError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class DuplicateEnrollmentError(Exception):
    pass


def get_all_enrollments(db: Session):
    statement = select(Enrollment)

    return db.scalars(statement).all()


def create_enrollment(
    db: Session,
    student_id: int,
    course_id: int
):
    # Check whether student exists
    student = db.get(Student, student_id)

    if student is None:
        raise StudentNotFoundError("Student not found")

    # Check whether course exists
    course = db.get(Course, course_id)

    if course is None:
        raise CourseNotFoundError("Course not found")

    # Check whether enrollment already exists
    statement = select(Enrollment).where(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    )

    existing_enrollment = db.scalars(statement).first()

    if existing_enrollment:
        raise DuplicateEnrollmentError(
            "Student is already enrolled in this course"
        )

    # Create enrollment
    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id
    )    

    try:
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

    except IntegrityError as error:
        db.rollback()

        raise DuplicateEnrollmentError(
            "Enrollment could not be created because of a database constraint"
        ) from error

    except Exception:
        db.rollback()
        raise

    return enrollment

class EnrollmentNotFoundError(Exception):
    pass


def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = db.get(Enrollment, enrollment_id)

    if enrollment is None:
        raise EnrollmentNotFoundError("Enrollment not found")

    try:
        db.delete(enrollment)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return enrollment