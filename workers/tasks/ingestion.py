"""
Tasks de ingestão de pedidos
"""
from celery import shared_task
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.session import SessionLocal
from src.database.models import Order
from src.operational_state.engine import OperationalStateEngine, OrderStateManager
from src.operational_state.events import EventPublisher, EventType, OperationalEventModel


@shared_task(bind=True, max_retries=3)
def normalize_order(self, order_id: str):
    """
    Normaliza um pedido recém-criado.
    
    1. Valida endereço
    2. Geocodifica (latitude/longitude)
    3. Enriquece dados
    4. Atualiza estado operacional
    5. Publica evento ORDER_NORMALIZED
    """
    db = SessionLocal()
    
    try:
        # Get order
        order = db.query(Order).filter(Order.id == UUID(order_id)).first()
        
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        # Normalize (placeholder - implement actual logic)
        normalized_data = {
            "address_valid": True,
            "geocoded": True,
            "enriched": True
        }
        
        # Update order
        order.operational_status = "normalized"
        order.address_latitude = order.address_latitude or -27.0  # Placeholder
        order.address_longitude = order.address_longitude or -52.0  # Placeholder
        
        db.commit()
        
        # Update operational state
        event_publisher = EventPublisher(db)
        engine = OperationalStateEngine(db, event_publisher)
        state_manager = OrderStateManager(engine)
        
        state_manager.mark_as_normalized(order.id, normalized_data)
        
        # Publish event
        event = OperationalEventModel(
            event_type=EventType.ORDER_NORMALIZED,
            source="/logisticsmart/normalization",
            subject=f"order/{order_id}",
            data=normalized_data,
            order_id=order.id
        )
        event_publisher.publish(event)
        
        return {"status": "success", "order_id": order_id}
    
    except Exception as e:
        # Retry on failure
        raise self.retry(exc=e, countdown=60)
    
    finally:
        db.close()


@shared_task
def process_webhook(webhook_data: dict):
    """
    Processa webhook de plataforma externa.
    
    1. Valida payload
    2. Cria pedido
    3. Dispara normalização
    """
    db = SessionLocal()
    
    try:
        # Create order (placeholder)
        order = Order(
            origin_platform=webhook_data.get("platform"),
            origin_order_id=webhook_data.get("order_id"),
            operational_status="created",
            # ... other fields
        )
        
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # Publish event
        event_publisher = EventPublisher(db)
        event_publisher.publish_order_created(order.id, webhook_data)
        
        return {"status": "success", "order_id": str(order.id)}
    
    finally:
        db.close()
