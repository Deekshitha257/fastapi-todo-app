from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    # Copy user data (contains email in "sub")
    to_encode = data.copy()
     # Set token expiry time (30 mins)
    expire = datetime.utcnow() + timedelta(
        minutes=30
    )
     # Add expiry to payload
    to_encode.update(
        {"exp": expire}
    )
    # Convert payload into signed JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
     # Return generated token
    return encoded_jwt



            # User Login
            #     ↓
            # {
            #     "sub": "deeku@gmail.com"
            # }
            #     ↓
            # Add Expiry
            #     ↓
            # {
            #     "sub": "deeku@gmail.com",
            #     "exp": "30 mins later"
            # }
            #     ↓
            # jwt.encode()
            #     ↓
            # eyJhbGciOiJIUzI1Ni...
            #     ↓
            # Return Token