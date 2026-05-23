import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.repositories import firebase_auth

client = TestClient(app)

@pytest.fixture
def unique_email():
    return f"api_test_{uuid.uuid4().hex[:8]}@example.com"

from unittest.mock import patch, MagicMock
from app.schemas.auth import UserInfo

def test_signup_endpoint(unique_email):
    with patch("app.repositories.firebase_auth.create_user") as mock_create:
        mock_create.return_value = UserInfo(
            uid="test-uid",
            email=unique_email,
            display_name="API Test User"
        )
        
        response = client.post(
            "/api/v1/auth/signup",
            json={"email": unique_email, "password": "Password123", "display_name": "API Test User"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == unique_email
        assert data["uid"] == "test-uid"

def test_signup_invalid_email():
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "not-an-email", "password": "Password123"}
    )
    assert response.status_code == 422 # Pydantic validation error

from unittest.mock import patch

def test_login_endpoint(unique_email):
    uid = "test-uid"
    
    with patch("app.repositories.firebase_auth.verify_id_token") as mock_verify, \
         patch("app.repositories.firebase_auth.get_user") as mock_get_user:
        
        mock_verify.return_value = {"uid": uid}
        mock_get_user.return_value = UserInfo(
            uid=uid,
            email=unique_email
        )
        
        response = client.post(
            "/api/v1/auth/login",
            json={"id_token": "valid-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["uid"] == uid
        assert data["email"] == unique_email

def test_login_invalid_token():
    with patch("app.repositories.firebase_auth.verify_id_token") as mock_verify:
        mock_verify.side_effect = firebase_auth.FirebaseError("Invalid token", "INVALID_TOKEN")
        
        response = client.post(
            "/api/v1/auth/login",
            json={"id_token": "invalid-token"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

def test_login_user_not_found():
    with patch("app.repositories.firebase_auth.verify_id_token") as mock_verify, \
         patch("app.repositories.firebase_auth.get_user") as mock_get_user:
        
        mock_verify.return_value = {"uid": "non-existent-uid"}
        mock_get_user.return_value = None
        
        response = client.post(
            "/api/v1/auth/login",
            json={"id_token": "valid-token-no-user"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "User not found"

def test_signup_duplicate_email(unique_email):
    with patch("app.repositories.firebase_auth.create_user") as mock_create:
        mock_create.side_effect = firebase_auth.FirebaseError("User already exists", "EMAIL_EXISTS")
        
        response = client.post(
            "/api/v1/auth/signup",
            json={"email": unique_email, "password": "Password123"}
        )
        assert response.status_code == 400
