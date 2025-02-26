# jwt_auth.py

from datetime import datetime, timedelta
from typing import Any, Dict
import hashlib
import configparser

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from util import flush_print
from mydb import MyDB

# Security settings
# IMPORTANT:  Do NOT use this in production.  This is for demonstration only.
# In production, you would want to store your secret key in an environment variable.

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Authentication Router
jwt_auth_router = APIRouter(prefix="/auth", tags=["authentication"])


# Initialize the database
my_db = MyDB("workspace/db.json")  # Initialize MyDB


# Load configuration from secret.ini
config = configparser.ConfigParser()
config.read('workspace/secret.ini')

# Get the secret key from secret.ini
SECRET_KEY = config.get('security', 'secret_key')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(username: str):
    """Retrieve user data based on username."""
    return my_db.get_user(username)


@jwt_auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint to obtain a JWT access token."""
    user = await get_user(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": form_data.username})
    flush_print(f"access token created")
    return {"access_token": access_token, "token_type": "bearer"}


# Example protected endpoint (requires authentication)
@jwt_auth_router.get("/protected")
async def protected_route():
    """Example protected route (requires a valid JWT access token)."""
    return {"message": "Successfully accessed protected route!"}