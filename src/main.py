import os
from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth_utils import authenticate_user, get_current_active_user, create_access_token
from src.models import Token
from src.routers import power_users, users

app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app.include_router(power_users.router)
app.include_router(users.router)


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
