from typing import Optional, Any
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from loguru import logger
from app.schemas.auth import UserCreate, UserUpdate, UserInfo


def verify_id_token(id_token: str) -> dict[str, Any]:
    """
    Verifies a Firebase ID token (JWT).
    Returns the decoded token dictionary if valid.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except FirebaseError as e:
        logger.error(f"Error verifying ID token: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid ID token: {e}")
        raise


def get_user(uid: str) -> Optional[UserInfo]:
    """
    Retrieves user information by UID.
    """
    try:
        user_record = auth.get_user(uid)
        return UserInfo(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            photo_url=user_record.photo_url,
            email_verified=user_record.email_verified,
            disabled=user_record.disabled
        )
    except auth.UserNotFoundError:
        return None
    except FirebaseError as e:
        logger.error(f"Error getting user {uid}: {e}")
        raise


def get_user_by_email(email: str) -> Optional[UserInfo]:
    """
    Retrieves user information by email.
    """
    try:
        user_record = auth.get_user_by_email(email)
        return UserInfo(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            photo_url=user_record.photo_url,
            email_verified=user_record.email_verified,
            disabled=user_record.disabled
        )
    except auth.UserNotFoundError:
        return None
    except FirebaseError as e:
        logger.error(f"Error getting user by email {email}: {e}")
        raise


def create_user(user_data: UserCreate) -> UserInfo:
    """
    Creates a new user in Firebase Authentication.
    """
    try:
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name,
            photo_url=user_data.photo_url,
            disabled=user_data.disabled
        )
        return UserInfo(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            photo_url=user_record.photo_url,
            email_verified=user_record.email_verified,
            disabled=user_record.disabled
        )
    except FirebaseError as e:
        logger.error(f"Error creating user: {e}")
        raise


def update_user(uid: str, user_data: UserUpdate) -> UserInfo:
    """
    Updates an existing user's information.
    """
    try:
        update_params = user_data.model_dump(exclude_none=True)
        user_record = auth.update_user(uid, **update_params)
        return UserInfo(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            photo_url=user_record.photo_url,
            email_verified=user_record.email_verified,
            disabled=user_record.disabled
        )
    except FirebaseError as e:
        logger.error(f"Error updating user {uid}: {e}")
        raise


def delete_user(uid: str) -> None:
    """
    Deletes a user from Firebase Authentication.
    """
    try:
        auth.delete_user(uid)
    except auth.UserNotFoundError:
        # Ignore if user already deleted
        pass
    except FirebaseError as e:
        logger.error(f"Error deleting user {uid}: {e}")
        raise


def create_custom_token(uid: str, developer_claims: Optional[dict] = None) -> str:
    """
    Creates a custom token for a given UID.
    """
    try:
        custom_token = auth.create_custom_token(uid, developer_claims)
        return custom_token.decode("utf-8")
    except FirebaseError as e:
        logger.error(f"Error creating custom token for {uid}: {e}")
        raise
