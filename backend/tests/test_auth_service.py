import pytest
import uuid
from pydantic import ValidationError
from app.services import auth_service
from app.schemas.auth import UserCreate
from app.repositories import firebase_auth

@pytest.fixture
def unique_email():
    return f"service_test_{uuid.uuid4().hex[:8]}@example.com"

@pytest.mark.asyncio
async def test_signup_success(unique_email):
    user_data = UserCreate(email=unique_email, password="Password123")
    user_info = await auth_service.signup(user_data)
    
    try:
        assert user_info.email == unique_email
        assert user_info.uid is not None
    finally:
        firebase_auth.delete_user(user_info.uid)

@pytest.mark.asyncio
async def test_signup_invalid_password(unique_email):
    # Short password
    with pytest.raises(ValidationError, match="at least 8 characters"):
        UserCreate(email=unique_email, password="Short1")
    
    # No uppercase
    with pytest.raises(ValueError, match="uppercase"):
        UserCreate(email=unique_email, password="password123")

@pytest.mark.asyncio
async def test_login_with_custom_token_success(unique_email):
    user_data = UserCreate(email=unique_email, password="Password123")
    user_info = await auth_service.signup(user_data)
    
    try:
        token = await auth_service.login_with_custom_token(unique_email)
        assert isinstance(token, str)
        assert len(token) > 0
    finally:
        firebase_auth.delete_user(user_info.uid)

@pytest.mark.asyncio
async def test_login_user_not_found():
    with pytest.raises(ValueError, match="User not found"):
        await auth_service.login_with_custom_token("non-existent@example.com")
