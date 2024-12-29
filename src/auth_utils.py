import os
from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from fastapi import status, HTTPException, Depends

from data_fetch.mongo_data_fetcher import MongoDBDataFetcher
from models import PowerUserInDB, TokenData, PowerUser

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# to get a string like this run:
# openssl rand -hex 32
# TODO : Make this part configurable, change this secret for production

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
mongo_connection_url = os.getenv("MONGO_CONNECTION_URL")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

power_user_data_fetcher = MongoDBDataFetcher(mongo_connection_url, "ski_planner", "power_users")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(username: str):
    user_details = power_user_data_fetcher.get_user_data(username)
    return PowerUserInDB(**user_details)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[PowerUser, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
