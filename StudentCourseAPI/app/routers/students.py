
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.student import StudentCreate, StudentResponse

from app.services.student_service import (
    get_all_students,
    get_student_by_id,
    create_student,
    create_my_student_profile,
    get_my_student_profile,
    StudentProfileAlreadyExists,
    StudentProfileNotFound
)

from app.core.dependencies import (
    get_db,
    require_admin,
    get_current_user
)


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# Admin only: Get all students
@router.get(
    "",
    response_model=list[StudentResponse],
    summary="Get all students",
    description="Retrieve students with pagination, searching, filtering, and sorting. Admin access required.",
    response_description="List of student records",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"}
    }
)
def get_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1),
    name: str | None = Query(default=None, min_length=1),
    sort_by: Literal["id", "name"] = "id",
    sort_order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_all_students(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        name=name,
        sort_by=sort_by,
        sort_order=sort_order
    )

# Admin only: Create a student
@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a student",
    description="Create a new student record. Only administrators can use this endpoint.",
    response_description="Successfully created student",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        409: {"description": "Student creation conflict"}
    }
)
def add_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    try:
        return create_student(db, student_data.name)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


# Create your own student profile
@router.post(
    "/me",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create my student profile",
    description="Create a student profile associated with the currently authenticated user.",
    response_description="Successfully created student profile",
    responses={
        401: {"description": "Authentication required"},
        409: {"description": "Student profile already exists"}
    }
)
def create_my_profile(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_my_student_profile(
            db=db,
            user_id=current_user.id,
            name=student_data.name
        )

    except StudentProfileAlreadyExists as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


# Get your own student profile
@router.get(
    "/me",
    response_model=StudentResponse,
    summary="Get my student profile",
    description="Retrieve the student profile belonging to the currently authenticated user.",
    response_description="Student profile",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "Student profile not found"}
    }
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_my_student_profile(
            db=db,
            user_id=current_user.id
        )

    except StudentProfileNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# Any authenticated user: Get your 
@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID",
    description="Retrieve a student by ID. Users can only access their own student profile.",
    response_description="Student record",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "Student not found or access not permitted"}
    }
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = get_student_by_id(
        db=db,
        student_id=student_id,
        user_id=current_user.id
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student
