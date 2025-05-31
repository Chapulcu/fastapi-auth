from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str  # email veya username olabilir
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
