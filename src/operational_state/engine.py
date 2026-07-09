"""
Operational State Engine - Conceito central do OCC
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session

from src.database.models import OperationalState, OperationalEvent
from src.operational_state.events import EventPublisher


class OperationalStateEngine:
    """
    Engine para gerenciar o estado operacional de entidades.
    
    Conceito OCC: Cada entidade (Order, Driver, Route, etc.) possui um estado
    cognitivo que representa o que o sistema "sabe", "acredita" e "pretende"
    sobre essa entidade.
    """
    
    def __init__(self, db: Session, event_publisher: EventPublisher):
        self.db = db
        self.event_publisher = event_publisher
    
    def get_current_state(self, entity_type: str, entity_id: UUID) -> Optional[OperationalState]:
        """Obtém o estado operacional atual de uma entidade"""
        return self.db.query(OperationalState).filter(
            OperationalState.entity_type == entity_type,
            OperationalState.entity_id == entity_id
        ).order_by(OperationalState.created_at.desc()).first()
    
    def update_state(
        self,
        entity_type: str,
        entity_id: UUID,
        representations: Optional[Dict] = None,
        knowledge: Optional[Dict] = None,
        beliefs: Optional[Dict] = None,
        decisions: Optional[Dict] = None,
        intentions: Optional[Dict] = None,
        confidence: float = 1.0,
        valid_until: Optional[datetime] = None,
        metadata: Optional[Dict] = None
    ) -> OperationalState:
        """
        Atualiza o estado operacional de uma entidade.
        
        Cria um novo estado com referência ao estado anterior (histórico).
        """
        # Get current state
        current_state = self.get_current_state(entity_type, entity_id)
        
        # Create new state
        new_state = OperationalState(
            entity_type=entity_type,
            entity_id=entity_id,
            representations=representations or (current_state.representations if current_state else {}),
            knowledge=knowledge or (current_state.knowledge if current_state else {}),
            beliefs=beliefs or (current_state.beliefs if current_state else {}),
            decisions=decisions or (current_state.decisions if current_state else {}),
            intentions=intentions or (current_state.intentions if current_state else {}),
            confidence=confidence,
            valid_until=valid_until,
            previous_state_id=current_state.id if current_state else None,
            metadata=metadata or {}
        )
        
        self.db.add(new_state)
        self.db.commit()
        self.db.refresh(new_state)
        
        return new_state
    
    def get_state_history(self, entity_type: str, entity_id: UUID, limit: int = 10) -> List[OperationalState]:
        """Obtém o histórico de estados de uma entidade"""
        return self.db.query(OperationalState).filter(
            OperationalState.entity_type == entity_type,
            OperationalState.entity_id == entity_id
        ).order_by(OperationalState.created_at.desc()).limit(limit).all()
    
    def decay_confidence(self, entity_type: str, entity_id: UUID, decay_rate: float = 0.1):
        """
        Aplica decaimento de confiança ao longo do tempo.
        
        Conceito OCC: Estados não confirmados perdem confiança ao longo do tempo.
        """
        current_state = self.get_current_state(entity_type, entity_id)
        
        if not current_state:
            return
        
        # Calculate time since last update
        time_elapsed = (datetime.utcnow() - current_state.updated_at).total_seconds() / 3600  # hours
        
        # Apply exponential decay
        new_confidence = current_state.confidence * (0.99 ** time_elapsed)
        
        # Update if confidence dropped significantly
        if new_confidence < current_state.confidence - 0.1:
            self.update_state(
                entity_type=entity_type,
                entity_id=entity_id,
                confidence=max(0.0, new_confidence)
            )
    
    def is_state_valid(self, entity_type: str, entity_id: UUID) -> bool:
        """Verifica se o estado operacional ainda é válido"""
        current_state = self.get_current_state(entity_type, entity_id)
        
        if not current_state:
            return False
        
        if current_state.valid_until and datetime.utcnow() > current_state.valid_until:
            return False
        
        if current_state.confidence < 0.5:
            return False
        
        return True


class OrderStateManager:
    """Gerenciador de estado específico para Orders"""
    
    def __init__(self, engine: OperationalStateEngine):
        self.engine = engine
    
    def mark_as_created(self, order_id: UUID, order_data: Dict):
        """Marca pedido como criado"""
        return self.engine.update_state(
            entity_type="order",
            entity_id=order_id,
            representations={"order_data": order_data},
            beliefs={"status": "created", "needs_normalization": True},
            intentions=["normalize", "validate_address"],
            confidence=1.0
        )
    
    def mark_as_normalized(self, order_id: UUID, normalized_data: Dict):
        """Marca pedido como normalizado"""
        return self.engine.update_state(
            entity_type="order",
            entity_id=order_id,
            representations={"normalized_data": normalized_data},
            beliefs={"status": "normalized", "needs_consolidation": True},
            intentions=["consolidate", "find_driver"],
            confidence=0.9
        )
    
    def mark_as_assigned(self, order_id: UUID, driver_id: UUID, route_id: UUID):
        """Marca pedido como atribuído"""
        return self.engine.update_state(
            entity_type="order",
            entity_id=order_id,
            beliefs={"status": "assigned", "driver_id": str(driver_id), "route_id": str(route_id)},
            intentions=["deliver"],
            confidence=0.95
        )
    
    def mark_as_delivered(self, order_id: UUID, delivery_data: Dict):
        """Marca pedido como entregue"""
        return self.engine.update_state(
            entity_type="order",
            entity_id=order_id,
            representations={"delivery_data": delivery_data},
            beliefs={"status": "delivered", "completed": True},
            intentions=["reconcile", "calculate_payment"],
            confidence=1.0
        )


class DriverStateManager:
    """Gerenciador de estado específico para Drivers"""
    
    def __init__(self, engine: OperationalStateEngine):
        self.engine = engine
    
    def mark_as_available(self, driver_id: UUID, location: Dict):
        """Marca motorista como disponível"""
        return self.engine.update_state(
            entity_type="driver",
            entity_id=driver_id,
            representations={"location": location},
            beliefs={"status": "available", "ready_for_orders": True},
            intentions=["accept_orders"],
            confidence=0.9
        )
    
    def mark_as_on_route(self, driver_id: UUID, route_id: UUID):
        """Marca motorista como em rota"""
        return self.engine.update_state(
            entity_type="driver",
            entity_id=driver_id,
            beliefs={"status": "on_route", "route_id": str(route_id)},
            intentions=["deliver_orders", "update_location"],
            confidence=0.95
        )
    
    def update_location(self, driver_id: UUID, location: Dict):
        """Atualiza localização do motorista"""
        current_state = self.engine.get_current_state("driver", driver_id)
        return self.engine.update_state(
            entity_type="driver",
            entity_id=driver_id,
            representations={"location": location},
            beliefs=current_state.beliefs if current_state else {},
            confidence=0.8  # Location data decays faster
        )
