from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse
)

from app.services.enrollment_service import (
    get_all_enrollments,
    create_enrollment,
    delete_enrollment,
    EnrollmentNotFoundError,
    StudentNotFoundError,
    CourseNotFoundError,
    DuplicateEnrollmentError
)


router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

# Get all enrollments
@router.get(
    "",
    response_model=list[EnrollmentResponse],
    summary="Get all enrollments",
    description="Retrieve all student-course enrollment records. Only administrators can access this endpoint.",
    response_description="List of enrollment records",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"}
    }
)
def get_enrollments(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_all_enrollments(db)


# Create an enrollment
@router.post(
    "",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an enrollment",
    description="Enroll a student in a course. Only administrators can perform this operation.",
    response_description="Successfully created enrollment",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        404: {"description": "Student or course not found"},
        409: {"description": "Student is already enrolled in this course"}
    }
)
def add_enrollment(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    try:
        return create_enrollment(
            db=db,
            student_id=enrollment_data.student_id,
            course_id=enrollment_data.course_id
        )

    except StudentNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except CourseNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except DuplicateEnrollmentError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


# Delete an enrollment
@router.delete(
    "/{enrollment_id}",
    summary="Delete an enrollment",
    description="Remove a student's enrollment using the enrollment ID. Only administrators can perform this operation.",
    response_description="Enrollment deletion confirmation",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        404: {"description": "Enrollment not found"}
    }
)
def remove_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    try:
        delete_enrollment(db, enrollment_id)

        return {
            "message": "Enrollment deleted successfully"
        }

    except EnrollmentNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )