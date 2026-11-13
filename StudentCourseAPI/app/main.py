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

logger = logging.getLogger("student_course_api")

# app = FastAPI(
#     title="Student Course API",
#     description="A structured FastAPI application",
#     version="1.0.0"
# )

app = FastAPI(
    title="Student Course Management API",
    description="""
    REST API for managing students, courses, enrollments,
    authentication, and role-based access control.

    Built with FastAPI, PostgreSQL, and SQLAlchemy.
    """,
    version="2.0.0",
    contact={
        "name": "API Support",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

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
    