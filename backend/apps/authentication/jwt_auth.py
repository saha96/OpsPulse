from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from ninja.security import HttpBearer

from .models import User


def generate_tokens(user: User) -> dict[str, str]:
    """Generate access and refresh tokens for authenticated user."""
    now = datetime.now(UTC)

    access_payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME_MINUTES),
    }

    refresh_payload = {
        "sub": str(user.id),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME_DAYS),
    }

    access_token = jwt.encode(access_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


class JWTAuth(HttpBearer):
    """Bearer token authentication for Django Ninja endpoints."""

    def authenticate(self, request, token: str) -> User | None:
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None

        user_id = payload.get("sub")
        try:
            user = User.objects.get(id=user_id, is_active=True)
            request.user = user
            return user
        except User.DoesNotExist:
            return None


class RoleRequired:
    """Dependency helper to enforce RBAC permissions."""

    def __init__(self, *allowed_roles: str):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User) -> bool:
        return user.role in self.allowed_roles or user.is_superuser
