from app.repositories import firebase_auth
from app.schemas.auth import UserCreate, UserInfo
from loguru import logger
from firebase_admin.exceptions import FirebaseError


async def signup(user_data: UserCreate) -> UserInfo:
    """
    Handles user registration.
    """
    try:
        logger.info(f"Attempting signup for user: {user_data.email}")
        user_info = firebase_auth.create_user(user_data)
        return user_info
    except FirebaseError as e:
        logger.error(f"Signup failed for {user_data.email}: {e}")
        raise
    except Exception:
        logger.exception(f"Unexpected error during signup for {user_data.email}")
        raise


async def login_with_custom_token(email: str) -> str:
    """
    Handles "login" by generating a custom token for a user found by email.
    Note: True login (password verification) is typically handled on the client-side
    using the Firebase Client SDK. The backend provides custom tokens for 
    trusted environments or administrative overrides.
    """
    try:
        logger.info(f"Generating custom token for: {email}")
        user = firebase_auth.get_user_by_email(email)
        if not user:
            logger.warning(f"Login failed: User not found for email {email}")
            raise ValueError("User not found")
        
        token = firebase_auth.create_custom_token(user.uid)
        return token
    except FirebaseError as e:
        logger.error(f"Token generation failed for {email}: {e}")
        raise
    except Exception:
        logger.exception(f"Unexpected error during login for {email}")
        raise
