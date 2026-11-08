from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import engine, Base, SessionLocal
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate, StudentResponse


app = FastAPI(title="FastAPI PostgreSQL Journey")


# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)


# Database session dependency
def get_db():       #FastAPI calls get_db() when an endpoint needs a database session.
    db = SessionLocal()

# The yield provides the session to the endpoint, and the finally block closes it after the request.

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "FastAPI connected to PostgreSQL!"}

# CREATE student
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = Student(**student.model_dump())

    db.add(new_student) #stages a new record for insertion.
    db.commit()             #commits the transaction, saving the new record to the database.
    db.refresh(new_student) #retrieves updated database values, including any auto-generated fields like id.   

    return new_student


# READ all students
@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    # Create a SELECT query for the Student model, sorted in ascending order by their ID
    query = select(Student).order_by(Student.id)
    #Executes the query and returns scalar results (the actual Python model instances instead of raw database rows/tuples).
    students = db.scalars(query).all()

    return students


# READ one student
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# UPDATE student
@app.patch("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


# DELETE student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}