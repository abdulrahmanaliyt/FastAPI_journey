from builtins import Exception

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Course
from .schemas import CourseCreate, CourseResponse, CourseUpdate

app = FastAPI(title="Course Management API - FastAPI PostgreSQL Journey")

# Create database tables automatically if they don't exist
Base.metadata.create_all(bind=engine)


# Database session dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.get("/")
def home():
  return {"message": "Course Management API connected to PostgreSQL!"}


# 1. CREATE a course
@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
# CRUD implementation
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
  new_course = Course(**course.model_dump())
  db.add(new_course)
  try:
    db.commit()
  except Exception:
    db.rollback()
    raise
  db.refresh(new_course)
  return new_course


# 2. READ all courses
@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
  query = select(Course).order_by(Course.id)
  courses = db.scalars(query).all()
  return courses


# 3. READ one course by ID
@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
  course = db.get(Course, course_id)
  if course is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
    )
  return course


# 4. PATCH - Update course details partially
@app.patch("/courses/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int, course: CourseUpdate, db: Session = Depends(get_db)
):
  db_course = db.get(Course, course_id)
  if not db_course:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
    )

  update_data = course.model_dump(exclude_unset=True, exclude_none=True)
  for key, value in update_data.items():
    setattr(db_course, key, value)

  db.commit()
  db.refresh(db_course)
  return db_course


# 5. DELETE a course
@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
  db_course = db.get(Course, course_id)
  if not db_course:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
    )

  db.delete(db_course)
  db.commit()
  return {
      "message": f"Course ID {course_id} deleted successfully",
      "deleted_course": {"id": db_course.id, "title": db_course.title},
  }