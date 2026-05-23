import pytest
import uuid
from app.repositories import firebase_auth
from app.schemas.auth import UserCreate, UserUpdate
from firebase_admin.exceptions import FirebaseError

from unittest.mock import patch, MagicMock

@pytest.fixture
def unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

def test_create_user_success(unique_email):
    user_data = UserCreate(email=unique_email, password="Password123", display_name="Test User")
    
    with patch("firebase_admin.auth.create_user") as mock_create:
        mock_create.return_value = MagicMock(
            uid="test-uid",
            email=unique_email,
            display_name="Test User",
            photo_url=None,
            email_verified=False,
            disabled=False
        )
        
        user_info = firebase_auth.create_user(user_data)
        assert user_info.uid == "test-uid"
        assert user_info.email == unique_email
        assert user_info.display_name == "Test User"

def test_get_user_success(unique_email):
    uid = "test-uid"
    with patch("firebase_admin.auth.get_user") as mock_get, \
         patch("firebase_admin.auth.get_user_by_email") as mock_get_email:
        
        mock_get.return_value = MagicMock(
            uid=uid,
            email=unique_email,
            display_name=None,
            photo_url=None,
            email_verified=False,
            disabled=False
        )
        mock_get_email.return_value = mock_get.return_value
        
        user_info = firebase_auth.get_user(uid)
        assert user_info is not None
        assert user_info.uid == uid
        
        user_by_email = firebase_auth.get_user_by_email(unique_email)
        assert user_by_email is not None
        assert user_by_email.uid == uid

def test_update_user_success(unique_email):
    uid = "test-uid"
    with patch("firebase_admin.auth.update_user") as mock_update:
        mock_update.return_value = MagicMock(
            uid=uid,
            email=unique_email,
            display_name="Updated Name",
            photo_url=None,
            email_verified=False,
            disabled=False
        )
        
        update_data = UserUpdate(display_name="Updated Name")
        updated_user = firebase_auth.update_user(uid, update_data)
        assert updated_user.display_name == "Updated Name"

def test_create_custom_token_success(unique_email):
    uid = "test-uid"
    with patch("firebase_admin.auth.create_custom_token") as mock_create_token:
        mock_create_token.return_value = b"mock-token"
        
        token = firebase_auth.create_custom_token(uid, {"admin": True})
        assert token == "mock-token"

# Edge Cases

def test_get_non_existent_user():
    with patch("firebase_admin.auth.get_user") as mock_get, \
         patch("firebase_admin.auth.get_user_by_email") as mock_get_email:
        
        from firebase_admin import auth
        mock_get.side_effect = auth.UserNotFoundError("Not found")
        mock_get_email.side_effect = auth.UserNotFoundError("Not found")
        
        user = firebase_auth.get_user("non-existent-uid")
        assert user is None
        
        user = firebase_auth.get_user_by_email("non-existent@example.com")
        assert user is None

def test_create_user_duplicate_email(unique_email):
    user_data = UserCreate(email=unique_email, password="Password123")
    
    with patch("firebase_admin.auth.create_user") as mock_create:
        mock_create.side_effect = FirebaseError("User already exists", "EMAIL_EXISTS")
        
        with pytest.raises(FirebaseError):
            firebase_auth.create_user(user_data)

def test_create_user_invalid_email():
    # Pydantic will catch this first if we use the schema
    with pytest.raises(Exception): # pydantic.ValidationError
        UserCreate(email="invalid-email", password="Password123")

def test_delete_non_existent_user():
    with patch("firebase_admin.auth.delete_user") as mock_delete:
        firebase_auth.delete_user("definitely-not-a-uid")
        mock_delete.assert_called_once()

def test_verify_invalid_token():
    with patch("firebase_admin.auth.verify_id_token") as mock_verify:
        mock_verify.side_effect = ValueError("Invalid token")
        with pytest.raises(ValueError):
            firebase_auth.verify_id_token("invalid-token")

def test_update_non_existent_user():
    update_data = UserUpdate(display_name="New Name")
    with patch("firebase_admin.auth.update_user") as mock_update:
        mock_update.side_effect = FirebaseError("User not found", "USER_NOT_FOUND")
        with pytest.raises(FirebaseError):
            firebase_auth.update_user("non-existent-uid", update_data)
