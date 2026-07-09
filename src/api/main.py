"""
FastAPI application for Agis REST API v3.0
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database.session import init_db
from src.utils.logger import setup_logging
from src.config.settings import settings

# Setup logging
setup_logging(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("🚀 Starting Agis API v3.0...")
    init_db()
    logger.info("✅ Database initialized")
    yield
    # Shutdown
    logger.info("🛑 Shutting down Agis API v3.0...")


# Create FastAPI app
app = FastAPI(
    title="Agis API",
    description="REST API for Agis v3.0 - Operational Cognitive Decision Platform",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Agis API",
        "version": "3.0.0",
        "environment": settings.APP_ENV
    }


# Include routers
from .routes import auth, deliveries, orders, drivers, routes

app.include_router(auth.router, prefix="/api/v1")
app.include_router(deliveries.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(drivers.router, prefix="/api/v1")
app.include_router(routes.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Agis API v3.0",
        "version": "3.0.0",
        "docs": "/docs",
        "health": "/health",
        "features": [
            "JWT Authentication",
            "Operational State Engine",
            "Event System (CloudEvents)",
            "Celery Workers",
            "PostgreSQL Database"
        ]
    }
