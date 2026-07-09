"""
Database models for LogisticSmart v3.0
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Text, Boolean, Float, 
    ForeignKey, JSON, Date, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default='viewer')  # admin, user, viewer
    active = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    deliveries = relationship("Delivery", back_populates="uploaded_by_user")
    reports = relationship("Report", back_populates="generated_by_user")
    audit_logs = relationship("AuditLog", back_populates="user")


class Delivery(Base):
    """Delivery data model."""
    __tablename__ = "deliveries"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500))
    file_size = Column(Integer)
    total_records = Column(Integer)
    processed_records = Column(Integer, default=0)
    status = Column(String(20), default='pending')  # pending, processing, completed, failed
    error_message = Column(Text)
    
    # Detected columns
    detected_columns = Column(JSON)
    
    # Metadata
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    # Relationships
    uploaded_by_user = relationship("User", back_populates="deliveries")
    reports = relationship("Report", back_populates="delivery")


class Report(Base):
    """Generated reports model."""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.id"))
    report_type = Column(String(50), nullable=False)  # excel, csv, pdf, docx
    file_path = Column(String(500))
    file_size = Column(Integer)
    filters_used = Column(JSON)
    
    # Statistics
    total_deliveries = Column(Integer)
    unique_deliverers = Column(Integer)
    date_range_start = Column(DateTime)
    date_range_end = Column(DateTime)
    
    # Metadata
    generated_by = Column(Integer, ForeignKey("users.id"))
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    delivery = relationship("Delivery", back_populates="reports")
    generated_by_user = relationship("User", back_populates="reports")


class AuditLog(Base):
    """Audit log for system actions."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)  # login, upload, export, delete
    resource_type = Column(String(50))  # delivery, report, user
    resource_id = Column(String(100))
    details = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")


# ═══════════════════════════════════════════════════════════════
# NOVOS MODELS (v3.0)
# ═══════════════════════════════════════════════════════════════

class Deposit(Base):
    """Depósito regional"""
    __tablename__ = "deposits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(2))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Contact
    phone = Column(String(20))
    email = Column(String(200))
    
    # Metadata
    meta_data = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="deposit")
    routes = relationship("Route", back_populates="deposit")
    
    __table_args__ = (
        Index('idx_deposits_city', 'city'),
    )


class Customer(Base):
    """Cliente final (destinatário)"""
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    phone = Column(String(20))
    document = Column(String(20))
    
    # Address (default)
    address_street = Column(String(200))
    address_number = Column(String(50))
    address_neighborhood = Column(String(100))
    address_city = Column(String(100))
    address_state = Column(String(2))
    address_zipcode = Column(String(10))
    address_latitude = Column(Float)
    address_longitude = Column(Float)
    
    # Learning metrics (OCC concept)
    total_deliveries = Column(Integer, default=0)
    successful_deliveries = Column(Integer, default=0)
    failed_deliveries = Column(Integer, default=0)
    avg_delivery_rating = Column(Float)
    
    # Preferences
    preferred_delivery_time = Column(String(50))  # morning, afternoon, evening
    special_instructions = Column(Text)
    
    # Metadata
    meta_data = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
    
    __table_args__ = (
        Index('idx_customers_phone', 'phone'),
        Index('idx_customers_city', 'address_city'),
    )


class Driver(Base):
    """Motorista"""
    __tablename__ = "drivers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    document = Column(String(20), nullable=False)
    
    # Vehicle
    vehicle_type = Column(String(50))  # motorcycle, car, van, truck_small, truck_medium
    vehicle_plate = Column(String(20))
    vehicle_capacity_kg = Column(Float)
    vehicle_capacity_m3 = Column(Float)
    
    # Operational state
    status = Column(String(50), default="offline")  # offline, available, on_route, on_break, inactive
    current_latitude = Column(Float)
    current_longitude = Column(Float)
    last_location_update = Column(DateTime)
    
    # Trust metrics (OCC concept)
    rating = Column(Float, default=5.0)
    completed_deliveries = Column(Integer, default=0)
    failed_deliveries = Column(Integer, default=0)
    avg_delivery_time_minutes = Column(Float)
    
    # Specialties (cities they know well)
    specialty_cities = Column(JSON)  # ["Chapecó", "Xanxerê", ...]
    
    # Metadata
    meta_data = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="driver")
    routes = relationship("Route", back_populates="driver")
    
    __table_args__ = (
        Index('idx_drivers_status', 'status'),
        Index('idx_drivers_phone', 'phone'),
    )


class Order(Base):
    """Pedido de entrega (conceito central)"""
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Origin
    origin_platform = Column(String(50))  # shoppi, shopee, mercadolivre, woocommerce, manual
    origin_order_id = Column(String(100))
    
    # Operational state (OCC concept)
    operational_status = Column(String(50), default="created")
    # created, normalized, consolidated, assigned, in_transit, delivered, failed, cancelled
    
    # Relationships
    deposit_id = Column(UUID(as_uuid=True), ForeignKey("deposits.id"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    
    # Delivery address
    address_street = Column(String(200))
    address_number = Column(String(50))
    address_complement = Column(String(100))
    address_neighborhood = Column(String(100))
    address_city = Column(String(100))
    address_state = Column(String(2))
    address_zipcode = Column(String(10))
    address_latitude = Column(Float)
    address_longitude = Column(Float)
    
    # Package
    weight_kg = Column(Float)
    length_cm = Column(Float)
    width_cm = Column(Float)
    height_cm = Column(Float)
    volume_m3 = Column(Float)
    
    # Financial
    declared_value_brl = Column(Float)
    shipping_cost_brl = Column(Float)
    
    # SLA
    promised_delivery_date = Column(DateTime)
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    
    # Special instructions
    special_instructions = Column(Text)
    
    # Assignment
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id"))
    driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.id"))
    
    # Delivery proof
    delivered_at = Column(DateTime)
    proof_photo_url = Column(String(500))
    proof_signature = Column(Text)
    delivery_notes = Column(Text)
    
    # Metadata
    meta_data = Column(JSON)  # Platform-specific data
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    deposit = relationship("Deposit", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    driver = relationship("Driver", back_populates="orders")
    route = relationship("Route", back_populates="orders")
    events = relationship("OperationalEvent", back_populates="order")
    states = relationship("OperationalState", back_populates="order",
                          primaryjoin="and_(Order.id==OperationalState.entity_id, OperationalState.entity_type=='order')",
                          foreign_keys="[OperationalState.entity_id]",
                          viewonly=True)
    
    __table_args__ = (
        Index('idx_orders_status', 'operational_status'),
        Index('idx_orders_deposit', 'deposit_id'),
        Index('idx_orders_customer', 'customer_id'),
        Index('idx_orders_driver', 'driver_id'),
        Index('idx_orders_route', 'route_id'),
        Index('idx_orders_city', 'address_city'),
        Index('idx_orders_promised_date', 'promised_delivery_date'),
    )


class Route(Base):
    """Rota de entrega"""
    __tablename__ = "routes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Assignment
    deposit_id = Column(UUID(as_uuid=True), ForeignKey("deposits.id"))
    driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.id"))
    
    # Operational state
    status = Column(String(50), default="planned")  # planned, in_progress, completed, cancelled
    
    # Metrics
    total_orders = Column(Integer, default=0)
    total_distance_km = Column(Float)
    estimated_duration_minutes = Column(Integer)
    actual_duration_minutes = Column(Integer)
    
    # Planning
    planned_date = Column(Date)
    
    # Execution
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Metadata
    meta_data = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    deposit = relationship("Deposit", back_populates="routes")
    driver = relationship("Driver", back_populates="routes")
    orders = relationship("Order", back_populates="route")
    
    __table_args__ = (
        Index('idx_routes_status', 'status'),
        Index('idx_routes_deposit', 'deposit_id'),
        Index('idx_routes_driver', 'driver_id'),
        Index('idx_routes_date', 'planned_date'),
    )


class OperationalEvent(Base):
    """Eventos operacionais (CloudEvents-compatible)"""
    __tablename__ = "operational_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # CloudEvents structure
    spec_version = Column(String(10), default="1.0")
    event_type = Column(String(100), nullable=False)
    source = Column(String(200))
    subject = Column(String(200))
    time = Column(DateTime, default=func.now())
    
    # Data
    data = Column(JSON)
    
    # Context
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.id"))
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id"))
    
    # Processing
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime)
    processing_error = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="events")
    
    __table_args__ = (
        Index('idx_events_type', 'event_type'),
        Index('idx_events_order', 'order_id'),
        Index('idx_events_processed', 'processed'),
        Index('idx_events_time', 'time'),
    )


class OperationalState(Base):
    """Estado operacional (OCC concept - coração do sistema)"""
    __tablename__ = "operational_states"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Entity reference
    entity_type = Column(String(50), nullable=False)  # order, driver, route, deposit
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Cognitive state (OCC concept)
    representations = Column(JSON)  # What the system "knows" about the entity
    knowledge = Column(JSON)        # Patterns and inferred relations
    beliefs = Column(JSON)          # Beliefs about the state
    decisions = Column(JSON)        # Decisions made
    intentions = Column(JSON)       # Planned actions
    
    # Confidence and validity
    confidence = Column(Float, default=1.0)
    valid_until = Column(DateTime)
    
    # History
    previous_state_id = Column(UUID(as_uuid=True), ForeignKey("operational_states.id"))
    
    # Metadata
    meta_data = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="states", foreign_keys=[entity_id],
                        primaryjoin="and_(OperationalState.entity_id==Order.id, OperationalState.entity_type=='order')",
                        viewonly=True)
    
    __table_args__ = (
        Index('idx_opstates_entity', 'entity_type', 'entity_id'),
        Index('idx_opstates_created', 'created_at'),
    )
