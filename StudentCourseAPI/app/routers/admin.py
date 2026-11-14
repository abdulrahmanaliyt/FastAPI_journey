from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.core.responses import success_response
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import UserResponse
from app.services.admin_service import get_all_users


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# admin router
@router.get(
    "/users",
    response_model=APIResponse,
    summary="Get all users",
    description="Retrieve a list of all registered users. This endpoint is restricted to administrators.",
    response_description="List of registered users",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"}
    }
)
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    users = get_all_users(db)
    return success_response(
        message="Users retrieved successfully",
        data=users
    )