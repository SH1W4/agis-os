"""
JWT Authentication Middleware for FastAPI
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.database.session import get_db
from src.database.models import User


security = HTTPBearer()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT de acesso.
    
    Args:
        data: Dados para incluir no token
        expires_delta: Tempo de expiração do token
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodifica um token JWT.
    
    Args:
        token: Token JWT a decodificar
        
    Returns:
        Dados decodificados do token
        
    Raises:
        HTTPException: Se o token for inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtém o usuário atual a partir do token JWT.
    
    Args:
        credentials: Credenciais HTTP com Bearer token
        db: Sessão do banco de dados
        
    Returns:
        Usuário autenticado
        
    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Obtém o usuário ativo atual.
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Usuário ativo
        
    Raises:
        HTTPException: Se o usuário não estiver ativo
    """
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return current_user


class JWTAuthMiddleware:
    """
    Middleware para autenticação JWT.
    
    Pode ser usado como dependência em endpoints FastAPI.
    """
    
    def __init__(self, required_roles: Optional[list] = None):
        """
        Inicializa o middleware.
        
        Args:
            required_roles: Lista de roles permitidas (opcional)
        """
        self.required_roles = required_roles or []
    
    async def __call__(
        self,
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """
        Verifica se o usuário tem as permissões necessárias.
        
        Args:
            current_user: Usuário atual
            
        Returns:
            Usuário autenticado
            
        Raises:
            HTTPException: Se o usuário não tiver as permissões necessárias
        """
        if self.required_roles and current_user.role not in self.required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {self.required_roles}"
            )
        
        return current_user


# Dependências comuns para uso nos endpoints
require_admin = JWTAuthMiddleware(required_roles=["admin"])
require_user = JWTAuthMiddleware(required_roles=["admin", "user"])
require_viewer = JWTAuthMiddleware(required_roles=["admin", "user", "viewer"])
