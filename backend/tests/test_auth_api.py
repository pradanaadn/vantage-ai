import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.repositories import firebase_auth

client = TestClient(app)

@pytest.fixture
def unique_email():
    return f"api_test_{uuid.uuid4().hex[:8]}@example.com"

def test_signup_endpoint(unique_email):
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": unique_email, "password": "Password123", "display_name": "API Test User"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert "uid" in data
    
    # Cleanup
    firebase_auth.delete_user(data["uid"])

def test_signup_invalid_email():
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "not-an-email", "password": "Password123"}
    )
    assert response.status_code == 422 # Pydantic validation error

def test_login_endpoint(unique_email):
    # First signup
    signup_response = client.post(
        "/api/v1/auth/signup",
        json={"email": unique_email, "password": "Password123"}
    )
    uid = signup_response.json()["uid"]
    
    try:
        # Then login
        response = client.post(f"/api/v1/auth/login?email={unique_email}")
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    finally:
        # Cleanup
        firebase_auth.delete_user(uid)

def test_login_user_not_found():
    response = client.post("/api/v1/auth/login?email=non-existent@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_signup_duplicate_email(unique_email):
    # First signup
    client.post(
        "/api/v1/auth/signup",
        json={"email": unique_email, "password": "Password123"}
    )
    
    try:
        # Second signup with same email
        response = client.post(
            "/api/v1/auth/signup",
            json={"email": unique_email, "password": "Password123"}
        )
        assert response.status_code == 400
    finally:
        # Cleanup
        user = firebase_auth.get_user_by_email(unique_email)
        if user:
            firebase_auth.delete_user(user.uid)
