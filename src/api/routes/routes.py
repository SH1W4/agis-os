"""
Route routes for API v3.0
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import date, datetime

from src.database.models import Route, Driver, Deposit
from src.database.session import get_db
from src.api.middleware.jwt_auth import get_current_active_user, require_admin
from src.database.models import User

router = APIRouter(prefix="/routes", tags=["routes"])


class RouteCreate(BaseModel):
    """Model for creating a new route"""
    deposit_id: UUID
    driver_id: UUID
    planned_date: date
    metadata: Optional[dict] = None


class RouteResponse(BaseModel):
    """Model for route response"""
    id: UUID
    deposit_id: UUID
    driver_id: UUID
    status: str
    total_orders: int
    total_distance_km: Optional[float]
    estimated_duration_minutes: Optional[int]
    actual_duration_minutes: Optional[int]
    planned_date: Optional[date]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new route.
    
    Args:
        route_data: Route data
        db: Database session
        current_user: Current authenticated user (admin only)
        
    Returns:
        Created route
    """
    # Verify driver exists
    driver = db.query(Driver).filter(Driver.id == route_data.driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    # Verify deposit exists
    deposit = db.query(Deposit).filter(Deposit.id == route_data.deposit_id).first()
    if not deposit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deposit not found"
        )
    
    # Create route
    route = Route(
        deposit_id=route_data.deposit_id,
        driver_id=route_data.driver_id,
        planned_date=route_data.planned_date,
        status="planned",
        meta_data=route_data.metadata
    )
    
    db.add(route)
    db.commit()
    db.refresh(route)
    
    return route


@router.get("/", response_model=List[RouteResponse])
async def list_routes(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    driver_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List routes with optional filters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by status
        driver_id: Filter by driver
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of routes
    """
    query = db.query(Route)
    
    if status:
        query = query.filter(Route.status == status)
    
    if driver_id:
        query = query.filter(Route.driver_id == driver_id)
    
    routes = query.order_by(Route.planned_date.desc()).offset(skip).limit(limit).all()
    
    return routes


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific route by ID.
    
    Args:
        route_id: Route ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Route details
    """
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    return route


@router.patch("/{route_id}/status")
async def update_route_status(
    route_id: UUID,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update route operational status.
    
    Args:
        route_id: Route ID
        new_status: New operational status
        db: Database session
        current_user: Current authenticated user (admin only)
        
    Returns:
        Updated route
    """
    valid_statuses = ["planned", "in_progress", "completed", "cancelled"]
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid statuses: {valid_statuses}"
        )
    
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    route.status = new_status
    
    if new_status == "in_progress" and not route.started_at:
        route.started_at = datetime.utcnow()
    elif new_status == "completed" and not route.completed_at:
        route.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(route)
    
    return route
