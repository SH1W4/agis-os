"""
Authentication routes for API v3.0 with JWT
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database.models import User
from src.database.session import get_db
from src.api.middleware.jwt_auth import create_access_token, get_current_active_user
from src.config.settings import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    Args:
        credentials: Login credentials
        db: Database session
        
    Returns:
        Login response with JWT token and user info
    """
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password (using bcrypt from existing auth system)
    from src.auth.authentication import AuthenticationManager
    auth_manager = AuthenticationManager()
    
    # Check if password matches
    success, _ = auth_manager.authenticate(
        credentials.username,
        credentials.password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "username": user.username,
            "name": user.name,
            "role": user.role,
            "email": user.email
        }
    )


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user information
    """
    return {
        "username": current_user.username,
        "name": current_user.name,
        "role": current_user.role,
        "email": current_user.email,
        "active": current_user.active,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None
    }
