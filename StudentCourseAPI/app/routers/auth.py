<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
=======
from fastapi import APIRouter, Depends, HTTPException, status, Request
>>>>>>> fcd3bc9eb5d783af70f09422dc8e947331f5d185
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.rate_limiter import limiter
from app.core.dependencies import get_db, get_current_user
from app.core.responses import success_response
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import UserCreate, UserResponse, Token

from fastapi import BackgroundTasks, Request

from app.tasks.notifications import send_welcome_notification
from app.services.auth_service import (
    register_user,
    authenticate_user,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Register
@router.post(
    "/register",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account using an email address and password.",
    response_description="Successfully registered user",
    responses={
        409: {"description": "Email address is already registered"},
        422: {"description": "Invalid registration data"}
    }
)
@limiter.limit("3/hour")
def register(
    request: Request,
<<<<<<< HEAD
    background_tasks: BackgroundTasks,
=======
>>>>>>> fcd3bc9eb5d783af70f09422dc8e947331f5d185
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        new_user = register_user(db, user_data)
        
        background_tasks.add_task(
            send_welcome_notification,
            new_user.email
        )
        
        return success_response(
            message="User registered successfully",
            data=new_user
        )

    except EmailAlreadyRegisteredError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


# Login
@router.post(
    "/login",
    response_model=APIResponse,
    summary="Login and obtain access token",
    description="""
    Authenticate a user using email and password.

    Submit credentials as form data:
    - username: Registered email address
    - password: Account password

    Returns a JWT access token that can be used
    to authenticate protected API requests.
    """,
    response_description="JWT access token",
    responses={
        401: {
            "description": "Invalid email or password",
            "headers": {
                "WWW-Authenticate": {
                    "description": "Bearer authentication challenge",
                    "schema": {"type": "string"}
                }
            }
        }
    }
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(
            db,
            form_data.username,
            form_data.password
        )

        access_token = create_access_token(user.id)

        return success_response(
            message="Login successful",
            data={
                "access_token": access_token,
                "token_type": "bearer"
            }
        )

    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"}
        )


# Get current user
@router.get(
    "/me",
    response_model=APIResponse,
    summary="Get current user",
    description="Retrieve the profile of the currently authenticated user using their JWT access token.",
    response_description="Authenticated user's profile",
    responses={
        401: {"description": "Invalid or missing access token"}
    }
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return success_response(
        message="User profile retrieved successfully",
        data=current_user
    )