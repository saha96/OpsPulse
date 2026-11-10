from datetime import datetime

from ninja import Schema
from pydantic import EmailStr


class LoginIn(Schema):
    username: str
    password: str


class RegisterIn(Schema):
    username: str
    email: EmailStr
    password: str
    department: str | None = "Platform Engineering"


class TokenOut(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenIn(Schema):
    refresh_token: str


class UserProfileOut(Schema):
    id: int
    username: str
    email: str
    role: str
    avatar_url: str | None = None
    department: str
    date_joined: datetime
