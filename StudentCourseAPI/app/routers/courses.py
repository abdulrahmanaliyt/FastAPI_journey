
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
    require_admin
)

from app.models.user import User

from app.schemas.course import (
    CourseCreate,
    CourseResponse
)

from app.services.course_service import (
    get_all_courses,
    create_course,
    update_course as update_course_service,
    delete_course
)


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


# Any authenticated user can view courses
@router.get("", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_courses(db)


# Only admin can create courses
@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return create_course(db, course_data)

@router.patch(
    "/{course_id}",
    response_model=CourseResponse
)

# Only admin can update courses
def update_course(
    course_id: int,
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    updated_course = update_course_service(db, course_id, course_data)

    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return updated_course

# Only admin can delete courses
@router.delete("/{course_id}")
def remove_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    deleted = delete_course(db, course_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return {
        "message": "Course deleted successfully"
    }
