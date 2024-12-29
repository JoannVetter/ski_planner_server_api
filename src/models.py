from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class PowerUser(BaseModel):
    username: str
    disabled: bool | None = None


class PowerUserInDB(PowerUser):
    hashed_password: str



