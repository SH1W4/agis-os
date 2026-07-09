"""
Driver routes for API v3.0
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from src.database.models import Driver
from src.database.session import get_db
from src.api.middleware.jwt_auth import get_current_active_user, require_admin
from src.database.models import User

router = APIRouter(prefix="/drivers", tags=["drivers"])


class DriverCreate(BaseModel):
    """Model for creating a new driver"""
    name: str
    phone: str
    document: str
    
    # Vehicle
    vehicle_type: Optional[str] = None
    vehicle_plate: Optional[str] = None
    vehicle_capacity_kg: Optional[float] = None
    vehicle_capacity_m3: Optional[float] = None
    
    # Specialties
    specialty_cities: Optional[List[str]] = None
    
    # Metadata
    metadata: Optional[dict] = None


class DriverResponse(BaseModel):
    """Model for driver response"""
    id: UUID
    name: str
    phone: str
    document: str
    vehicle_type: Optional[str]
    vehicle_plate: Optional[str]
    status: str
    rating: float
    completed_deliveries: int
    failed_deliveries: int
    avg_delivery_time_minutes: Optional[float]
    created_at: datetime
    updated_at: datetime


@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new driver.
    
    Args:
        driver_data: Driver data
        db: Database session
        current_user: Current authenticated user (admin only)
        
    Returns:
        Created driver
    """
    # Check if driver with same document already exists
    existing_driver = db.query(Driver).filter(Driver.document == driver_data.document).first()
    if existing_driver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver with this document already exists"
        )
    
    driver = Driver(
        name=driver_data.name,
        phone=driver_data.phone,
        document=driver_data.document,
        vehicle_type=driver_data.vehicle_type,
        vehicle_plate=driver_data.vehicle_plate,
        vehicle_capacity_kg=driver_data.vehicle_capacity_kg,
        vehicle_capacity_m3=driver_data.vehicle_capacity_m3,
        specialty_cities=driver_data.specialty_cities,
        meta_data=driver_data.metadata
    )
    
    db.add(driver)
    db.commit()
    db.refresh(driver)
    
    return driver


@router.get("/", response_model=List[DriverResponse])
async def list_drivers(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List drivers with optional filters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by status
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of drivers
    """
    query = db.query(Driver)
    
    if status:
        query = query.filter(Driver.status == status)
    
    drivers = query.order_by(Driver.created_at.desc()).offset(skip).limit(limit).all()
    
    return drivers


@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific driver by ID.
    
    Args:
        driver_id: Driver ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Driver details
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    return driver


@router.patch("/{driver_id}/status")
async def update_driver_status(
    driver_id: UUID,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update driver operational status.
    
    Args:
        driver_id: Driver ID
        new_status: New operational status
        db: Database session
        current_user: Current authenticated user (admin only)
        
    Returns:
        Updated driver
    """
    valid_statuses = ["offline", "available", "on_route", "on_break", "inactive"]
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid statuses: {valid_statuses}"
        )
    
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    driver.status = new_status
    db.commit()
    db.refresh(driver)
    
    return driver


@router.patch("/{driver_id}/location")
async def update_driver_location(
    driver_id: UUID,
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update driver location.
    
    Args:
        driver_id: Driver ID
        latitude: Current latitude
        longitude: Current longitude
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated driver
    """
    from datetime import datetime
    
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    driver.current_latitude = latitude
    driver.current_longitude = longitude
    driver.last_location_update = datetime.utcnow()
    
    db.commit()
    db.refresh(driver)
    
    # Publish event (if event system is enabled)
    try:
        from src.operational_state.events import EventPublisher
        event_publisher = EventPublisher(db)
        event_publisher.publish_driver_location(
            driver.id,
            {"latitude": latitude, "longitude": longitude}
        )
    except Exception as e:
        # Don't fail location update if event publishing fails
        pass
    
    return driver
