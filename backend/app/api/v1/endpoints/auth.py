from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserCreate, UserInfo
from app.services import auth_service
from firebase_admin.exceptions import FirebaseError
from loguru import logger

router = APIRouter()


@router.post("/signup", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """
    Register a new user.
    """
    try:
        return await auth_service.signup(user_data)
    except FirebaseError as e:
        logger.error(f"Signup API error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in signup endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.post("/login")
async def login(email: str):
    """
    Login and get a custom token.
    In a real app, this might be a GET or require password verification.
    """
    try:
        token = await auth_service.login_with_custom_token(email)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except FirebaseError as e:
        logger.error(f"Login API error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in login endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
