# Student Management API.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# 1. Define the student data structure

class Student(BaseModel):
    name: str
    course: str
    year: int


# 2. Define a model for partial updates

class StudentUpdate(BaseModel):
    name: str | None = None
    course: str | None = None
    year: int | None = None


# 3. Temporary student database

students = {
    1: {
        "name": "Rahul",
        "course": "CSE",
        "year": 3
    },
    2: {
        "name": "Aman",
        "course": "IT",
        "year": 2
    },
    3: {
            "name": "Abdul",
            "course": "cse",
            "year": 3
        }
}
courses=  ["CSE", "IT", "ECE", "ME"]

# 4. GET - Retrieve all students

@app.get("/students")
def get_students():
    return students
#--get all available courses
@app.get("/courses")
def all_courses():
    return {"courses": courses}
# _____________________

@app.get("/students/search")
def search_students(course: str):
    
    matching_students = {}
    
    
    for student_id, data in students.items():        
        if data["course"].lower() == course.lower():
            matching_students[student_id] = data
                
    if not matching_students:
        raise HTTPException(
            # status_code=404,
            status_code=200,
            detail=f"No students found for the course: {course}"
        )
        
    # return matching_students  #This is valid, but consider another approach:
    return list(matching_students.values())
# -----------------------------
# @app.get("/students/count")
# def total_student():
#     max_student = max(students.keys(), default=0)
#     return {"total_student":max_student}


#------------
# This gives you the highest student ID, not the total number of students.

# For example:
# students = {    1: {"name": "Rahul"},    5: {"name": "Aman"},    10: {"name": "Abdul"}}
#---------------------

#correct way 
@app.get("/students/count")
def total_student():
    return {
        "total_students": len(students)
    }

# ______________________
# 5. GET - Retrieve one student

@app.get("/students/{student_id}")
def get_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]


# 6. POST - Create a student

@app.post("/students", status_code=201)
def create_student(student: Student):

    new_id = max(students.keys(), default=0) + 1

    students[new_id] = student.model_dump()

    return {
        "message": "Student created successfully",
        "student_id": new_id,
        "student": students[new_id]
    }


# 7. PUT - Replace complete student details

@app.put("/students/{student_id}")
def replace_student(student_id: int, student: Student):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students[student_id] = student.model_dump()

    return {
        "message": "Student details replaced",
        "student": students[student_id]
    }


# 8. PATCH - Update selected student details

@app.patch("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentUpdate
):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student.model_dump(exclude_unset=True)

    students[student_id].update(update_data)

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }


# 9. DELETE - Remove a student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    deleted_student = students.pop(student_id)

    return {
        "message": f"Student id:{student_id} deleted successfully",
        "Student Deleted": deleted_student,
    }

