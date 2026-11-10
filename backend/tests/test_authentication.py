import pytest

from apps.authentication.models import User


@pytest.mark.django_db
class TestAuthenticationAPI:
    def test_register_success(self, client):
        payload = {
            "username": "newdev",
            "email": "newdev@opspulse.local",
            "password": "StrongPassword123!",
            "department": "Core Infrastructure",
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newdev"
        assert data["email"] == "newdev@opspulse.local"
        assert User.objects.filter(username="newdev").exists()

    def test_register_duplicate_username_fails(self, client, test_user):
        payload = {
            "username": test_user.username,
            "email": "different@opspulse.local",
            "password": "Password123!",
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 400
        assert "already taken" in response.json()["detail"]

    def test_login_success(self, client, test_user):
        response = client.post(
            "/auth/login",
            json={"username": test_user.username, "password": "ValidPassword123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "Bearer"

    def test_login_invalid_password_fails(self, client, test_user):
        response = client.post(
            "/auth/login",
            json={"username": test_user.username, "password": "WrongPassword!"},
        )
        assert response.status_code == 401

    def test_refresh_token_success(self, client, test_user):
        # 1. Login to get refresh token
        login_resp = client.post(
            "/auth/login",
            json={"username": test_user.username, "password": "ValidPassword123!"},
        )
        refresh_token = login_resp.json()["refresh_token"]

        # 2. Exchange refresh token
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_get_current_user_profile(self, client, auth_headers):
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testengineer"
        assert data["role"] == User.Role.ENGINEER

    def test_protected_route_without_token_rejected(self, client):
        response = client.get("/auth/me")
        assert response.status_code == 401
