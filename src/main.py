import os
from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from data_fetch.mongo_data_fetcher import MongoDBDataFetcher
from auth_utils import authenticate_user, get_current_active_user, create_access_token
from models import Token, PowerUser

app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO : Add this as a docker secret instead for safer option
mongo_connection_url = os.getenv("MONGO_CONNECTION_URL")
data_fetcher = MongoDBDataFetcher(mongo_connection_url, "ski_planner", "users")


@app.get("/users/{username}/friends")
async def get_user_friends(username: str, current_user: Annotated[PowerUser, Depends(get_current_active_user)]):
    return data_fetcher.get_user_friends(username)


@app.get("/users/{username}/equipment")
async def get_user_equipment(username: str, current_user: Annotated[PowerUser, Depends(get_current_active_user)]):
    return data_fetcher.get_user_equipment(username)


@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


if __name__ == "__main__":
    uvicorn.run(app)
