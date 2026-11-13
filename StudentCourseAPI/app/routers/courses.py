
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
    CourseUpdate,
    CourseReplace,
    CourseResponse
)

from app.services.course_service import (
    get_all_courses,
    create_course,
    update_course as update_course_service,
    delete_course,
    replace_course as replace_course_service
)


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


# Any authenticated user can view or Get all courses
@router.get(
    "",
    response_model=list[CourseResponse],
    summary="Get all courses",
    description="Retrieve all available courses. Any authenticated user can access this endpoint.",
    response_description="List of available courses",
    responses={
        401: {"description": "Authentication required"}
    }
)
def get_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_courses(db)


# Only admin can create courses
@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a course",
    description="Create a new course. Only administrators are authorized.",
    response_description="Successfully created course",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        409: {"description": "Course creation conflict"}
    }
)
def add_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return create_course(db, course_data)


# Only admin can update courses

@router.patch(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Update a course",
    description="Partially update an existing course. Only supplied fields are modified.",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        404: {"description": "Course not found"},
        422: {"description": "Invalid update data"}
    }
)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
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


# Change the complete course data
@router.put(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Replace a course",
    description="Replace all editable fields of an existing course. Only administrators can perform this operation.",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        404: {"description": "Course not found"},
        422: {"description": "Invalid replacement data"}
    }
)
def replace_course(
    course_id: int,
    course_data: CourseReplace,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    replaced_course = replace_course_service(
        db,
        course_id,
        course_data
    )

    if not replaced_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return replaced_course

# Only admin can delete courses
@router.delete(
    "/{course_id}",
    summary="Delete a course",
    description="Delete an existing course using its ID. Only administrators can perform this operation.",
    response_description="Course deletion confirmation",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        404: {"description": "Course not found"}
    }
)
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
