from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.core import get_current_user, create_access_token
from app.database import get_db
from app.models import User
from app.schemas import (
    LoginRequest,
    MessageResponse,
    TokenResponse,
    ForgetPasswordRequest,
    ResetPasswordRequest,
    UserCreate,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_name,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    if get_user_by_name(db, data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    return create_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(db, data.email, data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return TokenResponse(
        access_token=access_token,
    )


@router.get("/me", response_model=UserResponse)
def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user


@router.post("/logout", response_model=MessageResponse)
def logout():
    return MessageResponse(message="Successfully logged out")
