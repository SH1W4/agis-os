"""
Sistema de eventos operacionais (CloudEvents-compatible)
"""
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from src.database.models import OperationalEvent, Order, Driver, Route
from src.config.settings import settings


class EventType(str, Enum):
    """Tipos de eventos operacionais"""
    
    # Order events
    ORDER_CREATED = "logisticsmart.order.created"
    ORDER_NORMALIZED = "logisticsmart.order.normalized"
    ORDER_CONSOLIDATED = "logisticsmart.order.consolidated"
    ORDER_ASSIGNED = "logisticsmart.order.assigned"
    ORDER_IN_TRANSIT = "logisticsmart.order.in_transit"
    ORDER_DELIVERED = "logisticsmart.order.delivered"
    ORDER_FAILED = "logisticsmart.order.failed"
    ORDER_CANCELLED = "logisticsmart.order.cancelled"
    
    # Driver events
    DRIVER_AVAILABLE = "logisticsmart.driver.available"
    DRIVER_ON_ROUTE = "logisticsmart.driver.on_route"
    DRIVER_LOCATION_UPDATED = "logisticsmart.driver.location.updated"
    DRIVER_OFFLINE = "logisticsmart.driver.offline"
    
    # Route events
    ROUTE_CREATED = "logisticsmart.route.created"
    ROUTE_OPTIMIZED = "logisticsmart.route.optimized"
    ROUTE_STARTED = "logisticsmart.route.started"
    ROUTE_COMPLETED = "logisticsmart.route.completed"
    
    # System events
    SYSTEM_HEALTH_CHECK = "logisticsmart.system.health_check"
    SYSTEM_ERROR = "logisticsmart.system.error"


class OperationalEventModel:
    """Modelo de evento operacional (CloudEvents-compatible)"""
    
    def __init__(
        self,
        event_type: EventType,
        source: str,
        subject: str,
        data: Dict[str, Any],
        order_id: Optional[UUID] = None,
        driver_id: Optional[UUID] = None,
        route_id: Optional[UUID] = None
    ):
        self.spec_version = "1.0"
        self.id = str(uuid4())
        self.type = event_type.value
        self.source = source
        self.subject = subject
        self.time = datetime.utcnow()
        self.data = data
        self.order_id = order_id
        self.driver_id = driver_id
        self.route_id = route_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "specversion": self.spec_version,
            "id": self.id,
            "type": self.type,
            "source": self.source,
            "subject": self.subject,
            "time": self.time.isoformat(),
            "data": self.data
        }
    
    def to_db_model(self) -> OperationalEvent:
        """Converte para modelo de banco de dados"""
        return OperationalEvent(
            id=UUID(self.id),
            spec_version=self.spec_version,
            event_type=self.type,
            source=self.source,
            subject=self.subject,
            time=self.time,
            data=self.data,
            order_id=self.order_id,
            driver_id=self.driver_id,
            route_id=self.route_id
        )


class EventPublisher:
    """
    Publicador de eventos operacionais.
    
    Responsável por:
    1. Persistir eventos no banco de dados
    2. Disparar tasks Celery para processamento assíncrono
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.celery_app = None
    
    @property
    def celery_app(self):
        """Lazy load do Celery app"""
        if self.celery_app is None:
            from src.config.celery_config import celery_app
            self.celery_app = celery_app
        return self.celery_app
    
    def publish(self, event: OperationalEventModel) -> UUID:
        """
        Publica um evento operacional.
        
        1. Persiste no banco de dados
        2. Dispara task Celery para processamento
        """
        # 1. Persistir no banco
        db_event = event.to_db_model()
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        
        # 2. Disparar task Celery
        self.dispatch_handlers(event)
        
        return db_event.id
    
    def dispatch_handlers(self, event: OperationalEventModel):
        """Dispara handlers apropriados baseado no tipo de evento"""
        
        # Order events
        if event.type == EventType.ORDER_CREATED:
            self.celery_app.send_task(
                'workers.tasks.ingestion.normalize_order',
                args=[str(event.order_id)]
            )
        
        elif event.type == EventType.ORDER_NORMALIZED:
            self.celery_app.send_task(
                'workers.tasks.routing.consolidate_orders',
                args=[str(event.order_id)]
            )
        
        elif event.type == EventType.ORDER_CONSOLIDATED:
            self.celery_app.send_task(
                'workers.tasks.routing.optimize_route',
                args=[str(event.route_id)]
            )
        
        elif event.type == EventType.ORDER_ASSIGNED:
            self.celery_app.send_task(
                'workers.tasks.notifications.notify_driver',
                args=[str(event.driver_id), str(event.order_id)]
            )
        
        elif event.type == EventType.ORDER_DELIVERED:
            self.celery_app.send_task(
                'workers.tasks.notifications.notify_customer',
                args=[str(event.order_id)]
            )
            self.celery_app.send_task(
                'workers.tasks.reconciliation.calculate_payment',
                args=[str(event.order_id)]
            )
        
        # Driver events
        elif event.type == EventType.DRIVER_LOCATION_UPDATED:
            self.celery_app.send_task(
                'workers.tasks.tracking.update_tracking',
                args=[str(event.driver_id)]
            )
    
    def publish_order_created(self, order_id: UUID, order_data: Dict):
        """Helper para publicar evento de pedido criado"""
        event = OperationalEventModel(
            event_type=EventType.ORDER_CREATED,
            source="/logisticsmart/ingestion",
            subject=f"order/{order_id}",
            data=order_data,
            order_id=order_id
        )
        return self.publish(event)
    
    def publish_order_delivered(self, order_id: UUID, proof: Dict):
        """Helper para publicar evento de pedido entregue"""
        event = OperationalEventModel(
            event_type=EventType.ORDER_DELIVERED,
            source="/logisticsmart/delivery",
            subject=f"order/{order_id}",
            data={"proof": proof},
            order_id=order_id
        )
        return self.publish(event)
    
    def publish_driver_location(self, driver_id: UUID, location: Dict):
        """Helper para publicar evento de localização do motorista"""
        event = OperationalEventModel(
            event_type=EventType.DRIVER_LOCATION_UPDATED,
            source="/logisticsmart/tracking",
            subject=f"driver/{driver_id}",
            data=location,
            driver_id=driver_id
        )
        return self.publish(event)


class EventSubscriber:
    """
    Assinante de eventos operacionais.
    
    Responsável por processar eventos e atualizar o estado operacional.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_unprocessed_events(self, limit: int = 100) -> list:
        """Obtém eventos não processados"""
        return self.db.query(OperationalEvent).filter(
            OperationalEvent.processed == False
        ).order_by(OperationalEvent.time.asc()).limit(limit).all()
    
    def mark_as_processed(self, event_id: UUID):
        """Marca evento como processado"""
        event = self.db.query(OperationalEvent).filter(
            OperationalEvent.id == event_id
        ).first()
        
        if event:
            event.processed = True
            event.processed_at = datetime.utcnow()
            self.db.commit()
    
    def mark_as_failed(self, event_id: UUID, error: str):
        """Marca evento como falha"""
        event = self.db.query(OperationalEvent).filter(
            OperationalEvent.id == event_id
        ).first()
        
        if event:
            event.processing_error = error
            self.db.commit()
