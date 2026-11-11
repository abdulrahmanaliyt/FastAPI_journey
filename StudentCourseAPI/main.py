from sqlite3 import IntegrityError

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

from .database import engine, Base, SessionLocal
from .models import Student, Course, Enrollment
from .schemas import (
    StudentCreate,
    StudentResponse,
    CourseCreate,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    StudentWithCoursesResponse,
)

# Create tables in PostgreSQL automatically
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Course Enrollment API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome to the Student-Course Enrollment System!"}

@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.scalars(select(Student)).all()

# get students, courses, and enrollments endpoints
@app.get("/students-with-courses", response_model=list[StudentWithCoursesResponse])
def get_students_with_courses(db: Session = Depends(get_db)):
    # 1. Query students and eagerly load enrollments and their associated courses
    stmt = select(Student).options(selectinload(Student.enrollments).selectinload(Enrollment.course))
    students = db.scalars(stmt).all()

    # 2. Transform the data into the structure expected by StudentWithCoursesResponse
    result = []
    for student in students:
        course_titles = [
            enrollment.course.title 
            for enrollment in student.enrollments 
            if enrollment.course
        ]
        result.append({
            "id": student.id,
            "name": student.name,
            "courses": course_titles
        })

    return result

# --- 1. Students Endpoints ---
@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    student = Student(name=student_in.name)
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Database constraint violation")

    db.refresh(student)
    return student


# --- 2. Courses Endpoints ---
@app.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    course = Course(
        title=course_in.title, 
        duration=course_in.duration, 
        price=course_in.price
    )
    db.add(course)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"DATABASE ERROR: {e}")
        raise HTTPException(status_code=400, detail="Course with this title already exists")

    db.refresh(course)
    return course


@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.scalars(select(Course)).all()

@app.get("/enrollments", response_model=list[EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)):
    return db.scalars(select(Enrollment).options(joinedload(Enrollment.student), joinedload(Enrollment.course))).unique().all()

# --- 3. Enrollments Endpoints ---
@app.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment_in: EnrollmentCreate, db: Session = Depends(get_db)):
    # Verify student exists
    student = db.get(Student, enrollment_in.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Verify course exists
    course = db.get(Course, enrollment_in.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollment = Enrollment(
        student_id=enrollment_in.student_id,
        course_id=enrollment_in.course_id
    )
    db.add(enrollment)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")
    
    db.refresh(enrollment)
    return enrollment

# Transaction handling
@app.post("/enrollments/bulk", response_model=list[EnrollmentResponse], status_code=status.HTTP_201_CREATED)
def bulk_enroll_students(enrollments_in: list[EnrollmentCreate], db: Session = Depends(get_db)):
    enrollments = []
    try:
        for enrollment_in in enrollments_in:
            # Verify student exists
            student = db.get(Student, enrollment_in.student_id)
            if not student:
                raise HTTPException(status_code=404, detail=f"Student with ID {enrollment_in.student_id} not found")

            # Verify course exists
            course = db.get(Course, enrollment_in.course_id)
            if not course:
                raise HTTPException(status_code=404, detail=f"Course with ID {enrollment_in.course_id} not found")

            enrollment = Enrollment(
                student_id=enrollment_in.student_id,
                course_id=enrollment_in.course_id
            )
            db.add(enrollment)
            enrollments.append(enrollment)

        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to process enrollments")     
    for enrollment in enrollments:
        db.refresh(enrollment)
    return enrollments


# --- 4. Relationship Exploration Endpoints ---
@app.get("/students/{student_id}/courses")
def get_courses_for_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    stmt = (
        select(Student)
        .where(Student.id == student_id)
        .options(
            selectinload(Student.enrollments)
            .selectinload(Enrollment.course)
        )
    )

    student = db.scalars(stmt).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "student": student.name,
        "courses": [
            enrollment.course.title
            for enrollment in student.enrollments
        ]
    }

@app.get("/courses/{course_id}/students")
def get_students_for_course(course_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Course)
        .where(Course.id == course_id)
        .options(
            selectinload(Course.enrollments)
            .selectinload(Enrollment.student)
        )
    )

    course = db.scalars(stmt).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "course": course.title,
        "students": [
            enrollment.student.name
            for enrollment in course.enrollments
        ]
    }


# Assignment B — Cascade deletion
# Requirements:
# 1. Check whether the student exists.
# 2. Delete the student.
# 3. Ensure their enrollment records are also deleted.
# 4. Return a suitable response.
# 5. Verify the result in pgAdmin.

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student and associated enrollments deleted successfully"
    }
    