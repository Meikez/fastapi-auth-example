from typing import Annotated
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError

import models
from hashing_utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token,get_password_hash
from schemes import TokenData, User, Token, UserInDB
from database import get_user, users_db, Base, SessionLocal, engine

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# If it doesn't see an Authorization header,'
# 'it will respond with a 401 status code error (UNAUTHORIZED) directly.

# Initialize database
Base.metadata.create_all(engine)

# Functions


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ENDPOINTS
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user: UserInDB = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/register")
async def register(user_email: str, password: str):
    session = SessionLocal()
    user_exist = session.query(models.UserDB).filter_by(email=user_email).first()
    if user_exist:
        raise HTTPException(status_code=400,detail="Email already registered!")

    encrypted_password = get_password_hash(password)

    new_user = models.UserDB(email=user_email, password=encrypted_password)
    session.add(new_user)
    session.commit()
    session.close()


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/users/current")
async def read_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

