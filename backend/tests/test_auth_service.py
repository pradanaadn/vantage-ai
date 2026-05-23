import pytest
import uuid
from pydantic import ValidationError
from app.services import auth_service
from app.schemas.auth import UserCreate
from app.repositories import firebase_auth

from unittest.mock import patch, MagicMock
from app.schemas.auth import UserInfo, UserCreate
from app.services import auth_service
from app.repositories import firebase_auth

@pytest.fixture
def unique_email():
    return f"service_test_{uuid.uuid4().hex[:8]}@example.com"

@pytest.mark.asyncio
async def test_signup_success(unique_email):
    user_data = UserCreate(email=unique_email, password="Password123")
    
    with patch("app.repositories.firebase_auth.create_user") as mock_create:
        mock_create.return_value = UserInfo(
            uid="test-uid",
            email=unique_email
        )
        
        user_info = await auth_service.signup(user_data)
        assert user_info.email == unique_email
        assert user_info.uid == "test-uid"

@pytest.mark.asyncio
async def test_signup_invalid_password(unique_email):
    # Short password
    with pytest.raises(ValidationError, match="at least 8 characters"):
        UserCreate(email=unique_email, password="Short1")
    
    # No uppercase
    with pytest.raises(ValueError, match="uppercase"):
        UserCreate(email=unique_email, password="password123")

from unittest.mock import patch

@pytest.mark.asyncio
async def test_verify_token_success(unique_email):
    uid = "test-uid"
    
    with patch("app.repositories.firebase_auth.verify_id_token") as mock_verify, \
         patch("app.repositories.firebase_auth.get_user") as mock_get_user:
        
        mock_verify.return_value = {"uid": uid}
        mock_get_user.return_value = UserInfo(
            uid=uid,
            email=unique_email
        )
        
        verified_user = await auth_service.verify_token("valid-token")
        assert verified_user.uid == uid
        assert verified_user.email == unique_email

@pytest.mark.asyncio
async def test_verify_token_user_not_found():
    with patch("app.repositories.firebase_auth.verify_id_token") as mock_verify, \
         patch("app.repositories.firebase_auth.get_user") as mock_get_user:
        
        mock_verify.return_value = {"uid": "non-existent-uid"}
        mock_get_user.return_value = None
        
        with pytest.raises(ValueError, match="User not found"):
            await auth_service.verify_token("valid-token-but-no-user")
