from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import get_user_by_id


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Normal users to access their own profile.
# Administrators to access any user's profile.
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="""
    Retrieve a user profile using its ID.

    Authorization rules:
    - Normal users can access only their own profile.
    - Administrators can access any user's profile.
    """,
    response_description="Requested user profile",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "User not found or access not permitted"}
    }
)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Normal users can only access their own profile
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Retrieve requested user
    requested_user = get_user_by_id(db, user_id)

    if requested_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return requested_user