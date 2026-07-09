"""
Route assigner for LogisticSmart v3.0
Assigns orders to drivers based on various criteria
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.database.models import Order, Driver, Route
from src.routing.optimizer import RouteOptimizer, Point, DeliveryPoint


class RouteAssigner:
    """
    Atribuidor de rotas para motoristas.
    
    Responsável por:
    1. Selecionar motoristas disponíveis
    2. Atribuir pedidos a motoristas
    3. Criar rotas otimizadas
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o atribuidor.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.optimizer = RouteOptimizer()
    
    def assign_orders_to_driver(
        self,
        order_ids: List[UUID],
        driver_id: UUID,
        deposit_id: UUID
    ) -> Route:
        """
        Atribui uma lista de pedidos a um motorista e cria uma rota.
        
        Args:
            order_ids: Lista de IDs de pedidos
            driver_id: ID do motorista
            deposit_id: ID do depósito
            
        Returns:
            Rota criada
        """
        # Verificar se o motorista existe e está disponível
        driver = self.db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise ValueError(f"Driver {driver_id} not found")
        
        if driver.status != "available":
            raise ValueError(f"Driver {driver_id} is not available")
        
        # Buscar pedidos
        orders = self.db.query(Order).filter(Order.id.in_(order_ids)).all()
        if len(orders) != len(order_ids):
            raise ValueError("Some orders not found")
        
        # Buscar depósito
        deposit = self.db.query(Deposit).filter(Deposit.id == deposit_id).first()
        if not deposit:
            raise ValueError(f"Deposit {deposit_id} not found")
        
        # Criar pontos de entrega
        delivery_points = []
        for order in orders:
            if not order.address_latitude or not order.address_longitude:
                raise ValueError(f"Order {order.id} missing coordinates")
            
            point = DeliveryPoint(
                id=str(order.id),
                point=Point(order.address_latitude, order.address_longitude),
                priority=order.priority
            )
            delivery_points.append(point)
        
        # Otimizar rota
        start_point = Point(deposit.latitude or -27.0, deposit.longitude or -52.0)
        optimized_points = self.optimizer.optimize_route(start_point, delivery_points)
        
        # Calcular métricas
        metrics = self.optimizer.calculate_route_metrics(optimized_points, start_point)
        
        # Criar rota
        route = Route(
            deposit_id=deposit_id,
            driver_id=driver_id,
            status="planned",
            total_orders=len(orders),
            total_distance_km=metrics["total_distance_km"],
            estimated_duration_minutes=metrics["total_duration_minutes"],
            metadata={"optimized": True, "algorithm": "nearest_neighbor"}
        )
        
        self.db.add(route)
        self.db.commit()
        self.db.refresh(route)
        
        # Atualizar pedidos com a rota
        for order in orders:
            order.route_id = route.id
            order.driver_id = driver_id
            order.operational_status = "assigned"
        
        # Atualizar status do motorista
        driver.status = "on_route"
        
        self.db.commit()
        
        return route
    
    def find_best_driver_for_order(
        self,
        order_id: UUID,
        max_distance_km: float = 50.0
    ) -> Optional[Driver]:
        """
        Encontra o melhor motorista para um pedido.
        
        Args:
            order_id: ID do pedido
            max_distance_km: Distância máxima em km
            
        Returns:
            Melhor motorista encontrado ou None
        """
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        if not order.address_latitude or not order.address_longitude:
            return None
        
        # Buscar motoristas disponíveis
        available_drivers = self.db.query(Driver).filter(
            Driver.status == "available"
        ).all()
        
        if not available_drivers:
            return None
        
        # Se o motorista tiver especialidade na cidade, dar preferência
        city_drivers = [
            d for d in available_drivers
            if d.specialty_cities and order.address_city in d.specialty_cities
        ]
        
        if city_drivers:
            return city_drivers[0]
        
        # Caso contrário, retornar o primeiro disponível
        # Em produção, usar geolocalização real
        return available_drivers[0]
    
    def auto_assign_orders(
        self,
        order_ids: List[UUID],
        deposit_id: UUID
    ) -> List[Route]:
        """
        Atribui automaticamente pedidos aos melhores motoristas disponíveis.
        
        Args:
            order_ids: Lista de IDs de pedidos
            deposit_id: ID do depósito
            
        Returns:
            Lista de rotas criadas
        """
        routes = []
        remaining_orders = order_ids.copy()
        
        # Buscar motoristas disponíveis
        available_drivers = self.db.query(Driver).filter(
            Driver.status == "available"
        ).all()
        
        if not available_drivers:
            raise ValueError("No available drivers")
        
        # Distribuir pedidos entre motoristas
        orders_per_driver = len(remaining_orders) // len(available_drivers)
        
        for i, driver in enumerate(available_drivers):
            if not remaining_orders:
                break
            
            # Pegar pedidos para este motorista
            driver_orders = remaining_orders[:orders_per_driver]
            remaining_orders = remaining_orders[orders_per_driver:]
            
            # Atribuir
            try:
                route = self.assign_orders_to_driver(driver_orders, driver.id, deposit_id)
                routes.append(route)
            except Exception as e:
                print(f"Error assigning orders to driver {driver.id}: {e}")
        
        return routes
