from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt
from database import get_user


SECRET_KEY = "85eab742333eed5c1dfc27969da3e3b0f1a24c36d78d44655c1c4572a8616f48"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plaintext_password: str, hashed_password: str):
    return pwd_context.verify(plaintext_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(password: str, hashed_password: str):
    if not verify_password(password, hashed_password):
        return False
    return True


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

