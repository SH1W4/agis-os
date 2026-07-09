"""
Order routes for API v3.0
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.models import Order, Customer, Deposit
from src.database.session import get_db
from src.api.middleware.jwt_auth import get_current_active_user, require_admin
from src.database.models import User

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderCreate(BaseModel):
    """Model for creating a new order"""
    origin_platform: str
    origin_order_id: str
    customer_id: UUID
    deposit_id: UUID
    
    # Delivery address
    address_street: str
    address_number: str
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: str
    address_state: str
    address_zipcode: str
    address_latitude: Optional[float] = None
    address_longitude: Optional[float] = None
    
    # Package
    weight_kg: Optional[float] = None
    length_cm: Optional[float] = None
    width_cm: Optional[float] = None
    height_cm: Optional[float] = None
    volume_m3: Optional[float] = None
    
    # Financial
    declared_value_brl: Optional[float] = None
    shipping_cost_brl: Optional[float] = None
    
    # SLA
    promised_delivery_date: Optional[datetime] = None
    priority: str = "normal"
    
    # Special instructions
    special_instructions: Optional[str] = None
    
    # Metadata
    metadata: Optional[dict] = None


class OrderResponse(BaseModel):
    """Model for order response"""
    id: UUID
    origin_platform: str
    origin_order_id: str
    operational_status: str
    address_city: str
    address_state: str
    priority: str
    promised_delivery_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new order.
    
    Args:
        order_data: Order data
        db: Database session
        current_user: Current authenticated user (admin only)
        
    Returns:
        Created order
    """
    # Verify customer exists
    customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Verify deposit exists
    deposit = db.query(Deposit).filter(Deposit.id == order_data.deposit_id).first()
    if not deposit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deposit not found"
        )
    
    # Create order
    order = Order(
        origin_platform=order_data.origin_platform,
        origin_order_id=order_data.origin_order_id,
        operational_status="created",
        customer_id=order_data.customer_id,
        deposit_id=order_data.deposit_id,
        address_street=order_data.address_street,
        address_number=order_data.address_number,
        address_complement=order_data.address_complement,
        address_neighborhood=order_data.address_neighborhood,
        address_city=order_data.address_city,
        address_state=order_data.address_state,
        address_zipcode=order_data.address_zipcode,
        address_latitude=order_data.address_latitude,
        address_longitude=order_data.address_longitude,
        weight_kg=order_data.weight_kg,
        length_cm=order_data.length_cm,
        width_cm=order_data.width_cm,
        height_cm=order_data.height_cm,
        volume_m3=order_data.volume_m3,
        declared_value_brl=order_data.declared_value_brl,
        shipping_cost_brl=order_data.shipping_cost_brl,
        promised_delivery_date=order_data.promised_delivery_date,
        priority=order_data.priority,
        special_instructions=order_data.special_instructions,
        meta_data=order_data.metadata
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Publish event (if event system is enabled)
    try:
        from src.operational_state.events import EventPublisher, EventType
        event_publisher = EventPublisher(db)
        event_publisher.publish_order_created(
            order.id,
            {"platform": order.origin_platform, "order_id": order.origin_order_id}
        )
    except Exception as e:
        # Don't fail order creation if event publishing fails
        pass
    
    return order


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    city: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List orders with optional filters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by operational status
        city: Filter by city
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of orders
    """
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.operational_status == status)
    
    if city:
        query = query.filter(Order.address_city == city)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific order by ID.
    
    Args:
        order_id: Order ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Order details
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: UUID,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update order operational status.
    
    Args:
        order_id: Order ID
        new_status: New operational status
        db: Database session
        current_user: Current authenticated user (admin only)
        
    Returns:
        Updated order
    """
    valid_statuses = ["created", "normalized", "consolidated", "assigned", "in_transit", "delivered", "failed", "cancelled"]
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid statuses: {valid_statuses}"
        )
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.operational_status = new_status
    
    if new_status == "delivered":
        order.delivered_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    return order
