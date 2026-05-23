from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    disabled: bool = False

class UserCreate(UserBase):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
class UserInfo(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    email_verified: bool = False
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    disabled: bool = False

class LoginRequest(BaseModel):
    id_token: str

class TokenData(BaseModel):
    uid: str
    email: Optional[str] = None

