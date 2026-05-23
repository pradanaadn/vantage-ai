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


async def verify_token(id_token: str) -> UserInfo:
    """
    Verifies a Firebase ID token and returns the user info.
    """
    try:
        logger.info("Verifying ID token")
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token.get("uid")
        
        user_info = firebase_auth.get_user(uid) # type: ignore
        if not user_info:
            logger.warning(f"User not found for uid {uid}")
            raise ValueError("User not found")
        
        return user_info
    except FirebaseError as e:
        logger.error(f"Token verification failed: {e}")
        raise
    except Exception:
        logger.exception("Unexpected error during token verification")
        raise
