from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.users import UserCreate ,UserLogin
from app.core.security import hash_password ,verify_password
from app.core.auth import create_access_token
from fastapi import HTTPException

def register_user_service(
    user: UserCreate,
    db: Session
):
    hashed_password = hash_password(
        user.password
    )

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def login_user_service(
    user: UserLogin,
    db: Session
):
    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }    