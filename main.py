# main.py
from fastapi import FastAPI
from models import StudentCreate, StudentResponse, students

app = FastAPI()

# Register a new student
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=201
)
def register_student(student: StudentCreate):
    new_student = {
        "id": len(students) + 1,
        **student.model_dump()
    }
    students.append(new_student)
    return new_student


# Retrieve all students
@app.get("/students", response_model=list[StudentResponse])
def get_students():
    return students