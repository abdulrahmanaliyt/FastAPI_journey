import logging
from fastapi import FastAPI,Request,HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.responses import (
    success_response,
    error_response
)
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

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            error_response(str(exc.detail))
        ),
        headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = [
        {
            "field": ".".join(str(item) for item in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            error_response(
                message="Request validation failed",
                data=errors
            )
        )
    )

# Golbal exception handler
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
        ontent=error_response("Internal server error")
    )
    
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/")
def home():
    return success_response(
        message="Student Course API is running"
    )