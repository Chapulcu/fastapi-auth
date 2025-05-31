from sqlalchemy.orm import Session
from typing import Optional
from ..models.user import User
from ..utils.security import verify_password, create_access_token, create_refresh_token
from .user import get_user_by_username, get_user_by_email

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    # Username veya email ile giriş yapabilir
    user = get_user_by_username(db, username)
    if not user:
        user = get_user_by_email(db, username)
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user

def create_tokens(user: User) -> dict:
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
