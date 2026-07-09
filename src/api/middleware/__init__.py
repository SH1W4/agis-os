"""
API middleware for LogisticSmart v3.0
"""
from src.api.middleware.jwt_auth import JWTAuthMiddleware

__all__ = ['JWTAuthMiddleware']
