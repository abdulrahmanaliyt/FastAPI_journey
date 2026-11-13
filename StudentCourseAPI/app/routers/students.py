
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
@router.get("", response_model=list[StudentResponse])
def get_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_all_students(
        db=db,
        skip=skip,
        limit=limit
    )

# Admin only: Create a student
@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
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
    status_code=status.HTTP_201_CREATED
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
    response_model=StudentResponse
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


# Any authenticated user: Get one student
@router.get("/{student_id}", response_model=StudentResponse)
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
