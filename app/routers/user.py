from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.users import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token
)
from app.services.user_service import (
    register_user_service,
    login_user_service
)
from app.dependencies.auth import get_current_user
from app.models.user import User
router = APIRouter( prefix="/users",
    tags=["Users"])

@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user_service(
        user=user,
        db=db
    )

@router.post(
    "/login",
    response_model=Token
)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user_service(
        user=user,
        db=db
    )    

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user    