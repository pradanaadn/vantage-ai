from fastapi import Header, HTTPException, status
from app.schemas.auth import UserInfo
from app.services import auth_service


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> UserInfo:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
        )

    id_token = authorization.removeprefix("Bearer ").strip()
    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
        )

    try:
        return await auth_service.verify_token(id_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
