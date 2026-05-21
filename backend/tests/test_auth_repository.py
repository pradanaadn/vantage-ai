import pytest
import uuid
from app.repositories import firebase_auth
from app.schemas.auth import UserCreate, UserUpdate
from firebase_admin.exceptions import FirebaseError

@pytest.fixture
def unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

def test_create_user_success(unique_email):
    user_data = UserCreate(email=unique_email, password="password123", display_name="Test User")
    user_info = firebase_auth.create_user(user_data)
    
    try:
        assert user_info.uid is not None
        assert user_info.email == unique_email
        assert user_info.display_name == "Test User"
    finally:
        firebase_auth.delete_user(user_info.uid)

def test_get_user_success(unique_email):
    user_data = UserCreate(email=unique_email, password="password123")
    created_user = firebase_auth.create_user(user_data)
    
    try:
        user_info = firebase_auth.get_user(created_user.uid)
        assert user_info is not None
        assert user_info.uid == created_user.uid
        
        user_by_email = firebase_auth.get_user_by_email(unique_email)
        assert user_by_email is not None
        assert user_by_email.uid == created_user.uid
    finally:
        firebase_auth.delete_user(created_user.uid)

def test_update_user_success(unique_email):
    user_data = UserCreate(email=unique_email, password="password123")
    created_user = firebase_auth.create_user(user_data)
    
    try:
        update_data = UserUpdate(display_name="Updated Name")
        updated_user = firebase_auth.update_user(created_user.uid, update_data)
        assert updated_user.display_name == "Updated Name"
    finally:
        firebase_auth.delete_user(created_user.uid)

def test_create_custom_token_success(unique_email):
    user_data = UserCreate(email=unique_email, password="password123")
    created_user = firebase_auth.create_user(user_data)
    
    try:
        token = firebase_auth.create_custom_token(created_user.uid, {"admin": True})
        assert isinstance(token, str)
        assert len(token) > 0
    finally:
        firebase_auth.delete_user(created_user.uid)

# Edge Cases

def test_get_non_existent_user():
    user = firebase_auth.get_user("non-existent-uid")
    assert user is None
    
    user = firebase_auth.get_user_by_email("non-existent@example.com")
    assert user is None

def test_create_user_duplicate_email(unique_email):
    user_data = UserCreate(email=unique_email, password="password123")
    created_user = firebase_auth.create_user(user_data)
    
    try:
        with pytest.raises(FirebaseError):
            firebase_auth.create_user(user_data)
    finally:
        firebase_auth.delete_user(created_user.uid)

def test_create_user_invalid_email():
    # Pydantic will catch this first if we use the schema
    with pytest.raises(Exception): # pydantic.ValidationError
        UserCreate(email="invalid-email", password="password123")

def test_delete_non_existent_user():
    # Firebase Admin SDK delete_user does not raise an error if the user doesn't exist
    # It just succeeds silently.
    firebase_auth.delete_user("definitely-not-a-uid")

def test_verify_invalid_token():
    with pytest.raises(Exception): # ValueError or FirebaseError
        firebase_auth.verify_id_token("invalid-token")

def test_update_non_existent_user():
    update_data = UserUpdate(display_name="New Name")
    with pytest.raises(FirebaseError):
        firebase_auth.update_user("non-existent-uid", update_data)
