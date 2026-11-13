import logging
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

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

logger = logging.getLogger("student_course_api")

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
    
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )