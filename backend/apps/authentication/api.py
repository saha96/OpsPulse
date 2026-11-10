from django.contrib.auth import authenticate
from ninja import Router
from ninja.errors import HttpError

from .jwt_auth import JWTAuth, decode_token, generate_tokens
from .models import User
from .schemas import LoginIn, RefreshTokenIn, RegisterIn, TokenOut, UserProfileOut

router = Router()
auth_required = JWTAuth()


@router.post("/login", response=TokenOut, auth=None)
def login(request, data: LoginIn):
    """Authenticate user with username/password and return JWT tokens."""
    user = authenticate(username=data.username, password=data.password)
    if not user:
        raise HttpError(401, "Invalid username or password.")
    if not user.is_active:
        raise HttpError(403, "Account is disabled.")

    return generate_tokens(user)


@router.post("/register", response=UserProfileOut, auth=None)
def register(request, data: RegisterIn):
    """Register a new user account."""
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username already taken.")
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email already registered.")

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        department=data.department or "Platform Engineering",
        role=User.Role.ENGINEER,
    )
    return user


@router.post("/refresh", response=TokenOut, auth=None)
def refresh_token(request, data: RefreshTokenIn):
    """Exchange a valid refresh token for a new token pair."""
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HttpError(401, "Invalid or expired refresh token.")

    user_id = payload.get("sub")
    try:
        user = User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist as exc:
        raise HttpError(401, "User no longer exists.") from exc

    return generate_tokens(user)


@router.get("/me", response=UserProfileOut, auth=auth_required)
def get_current_user(request):
    """Retrieve profile of the currently authenticated user."""
    return request.user
