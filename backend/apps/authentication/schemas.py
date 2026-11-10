from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginIn(BaseModel):
    username: str
    password: str


class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    department: str | None = "Platform Engineering"


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenIn(BaseModel):
    refresh_token: str


class UserProfileOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    avatar_url: str | None = None
    department: str
    date_joined: datetime
