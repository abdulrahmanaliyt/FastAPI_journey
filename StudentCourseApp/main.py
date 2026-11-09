from builtins import Exception

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
)

# Create tables in PostgreSQL automatically
Base.metadata.create_all(bind=engine)

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


# --- 1. Students Endpoints ---
@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    student = Student(name=student_in.name)
    db.add(student)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student with this name already exists")

    db.refresh(student)
    return student


@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.scalars(select(Student)).all()


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
        raise HTTPException(status_code=400, detail=str(e))

    db.refresh(course)
    return course


@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.scalars(select(Course)).all()


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


# --- 4. Relationship Exploration Endpoints ---
@app.get("/students/{student_id}/courses")
def get_courses_for_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Access the courses through the enrollment relationship list
    courses = [enrollment.course for enrollment in student.enrollments]
    return {"student": student.name, "courses": courses}


@app.get("/courses/{course_id}/students")
def get_students_for_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Access the students through the enrollment relationship list
    students = [enrollment.student for enrollment in course.enrollments]
    return {"course": course.title, "students": students}