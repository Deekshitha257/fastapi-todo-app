from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os

from app.dependencies.database import get_db
from app.models.user import User

# Extracts JWT token from Authorization header
oauth2_scheme = HTTPBearer()

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="login"
# )

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(
    # Automatically gets Authorization: Bearer <token> from request
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        # Verifies token and retrieves stored payload data
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        # Extracts user email stored under JWT "sub" claim
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
# Finds the logged-in user in database using email from token
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user