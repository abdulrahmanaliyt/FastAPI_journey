from fastapi import FastAPI

from app.routers import (
    auth,
    users,
    students,
    courses,
    enrollments,
    admin
)

app = FastAPI(
    title="Student Course API",
    description="A structured FastAPI application",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {
        "message": "Student Course API is running"
    }