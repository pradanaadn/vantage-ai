from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserCreate, UserInfo, LoginRequest
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


@router.post("/login", response_model=UserInfo)
async def login(request: LoginRequest):
    """
    Verify a Firebase ID token and login.
    """
    try:
        return await auth_service.verify_token(request.id_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except FirebaseError as e:
        logger.error(f"Login API error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        logger.exception("Unexpected error in login endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
