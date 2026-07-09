"""
Payment calculator for LogisticSmart v3.0
Calculates driver payments and delivery costs
"""
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.database.models import Order, Driver, Route


class PaymentCalculator:
    """
    Calculadora de pagamentos para LogisticSmart v3.0.
    
    Responsável por:
    1. Calcular pagamento por entrega
    2. Calcular bônus por performance
    3. Calcular deduções por atrasos/erros
    4. Gerar relatório de pagamentos
    """
    
    # Taxas base (configurável)
    BASE_RATE_PER_DELIVERY = 5.0  # R$ por entrega
    RATE_PER_KM = 0.5  # R$ por km
    BONUS_PER_RATING_POINT = 1.0  # Bônus por ponto de rating
    PENALTY_PER_DELAY_HOUR = 2.0  # Penalidade por hora de atraso
    
    def __init__(self, db: Session):
        """
        Inicializa a calculadora.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
    
    def calculate_delivery_payment(
        self,
        order_id: str
    ) -> Dict[str, Any]:
        """
        Calcula pagamento por uma entrega específica.
        
        Args:
            order_id: ID do pedido
            
        Returns:
            Dicionário com detalhes do pagamento
        """
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if not order.delivered_at:
            raise ValueError(f"Order {order_id} not delivered yet")
        
        # Pagamento base por entrega
        base_payment = self.BASE_RATE_PER_DELIVERY
        
        # Bônus por distância (se disponível)
        distance_bonus = 0.0
        if order.route_id:
            route = self.db.query(Route).filter(Route.id == order.route_id).first()
            if route and route.total_distance_km:
                distance_bonus = route.total_distance_km * self.RATE_PER_KM
        
        # Bônus por rating do motorista
        rating_bonus = 0.0
        if order.driver_id:
            driver = self.db.query(Driver).filter(Driver.id == order.driver_id).first()
            if driver:
                rating_bonus = (driver.rating - 4.0) * self.BONUS_PER_RATING_POINT
                if rating_bonus < 0:
                    rating_bonus = 0
        
        # Penalidade por atraso
        delay_penalty = 0.0
        if order.promised_delivery_date and order.delivered_at:
            delay_hours = (order.delivered_at - order.promised_delivery_date).total_seconds() / 3600
            if delay_hours > 0:
                delay_penalty = delay_hours * self.PENALTY_PER_DELAY_HOUR
        
        # Total
        total_payment = base_payment + distance_bonus + rating_bonus - delay_penalty
        
        return {
            "order_id": str(order_id),
            "driver_id": str(order.driver_id) if order.driver_id else None,
            "base_payment": round(base_payment, 2),
            "distance_bonus": round(distance_bonus, 2),
            "rating_bonus": round(rating_bonus, 2),
            "delay_penalty": round(delay_penalty, 2),
            "total_payment": round(max(0, total_payment), 2),
            "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None
        }
    
    def calculate_driver_period_payment(
        self,
        driver_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Calcula pagamento total de um motorista em um período.
        
        Args:
            driver_id: ID do motorista
            start_date: Data inicial do período
            end_date: Data final do período
            
        Returns:
            Dicionário com detalhes do pagamento do período
        """
        # Buscar entregas do motorista no período
        orders = self.db.query(Order).filter(
            Order.driver_id == driver_id,
            Order.delivered_at >= start_date,
            Order.delivered_at <= end_date,
            Order.operational_status == "delivered"
        ).all()
        
        if not orders:
            return {
                "driver_id": driver_id,
                "total_deliveries": 0,
                "total_payment": 0.0,
                "details": []
            }
        
        # Calcular pagamento para cada entrega
        payments = []
        total_payment = 0.0
        
        for order in orders:
            try:
                payment = self.calculate_delivery_payment(str(order.id))
                payments.append(payment)
                total_payment += payment["total_payment"]
            except Exception as e:
                print(f"Error calculating payment for order {order.id}: {e}")
        
        return {
            "driver_id": driver_id,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "total_deliveries": len(orders),
            "total_payment": round(total_payment, 2),
            "details": payments
        }
    
    def calculate_route_payment(
        self,
        route_id: str
    ) -> Dict[str, Any]:
        """
        Calcula pagamento total por uma rota.
        
        Args:
            route_id: ID da rota
            
        Returns:
            Dicionário com detalhes do pagamento da rota
        """
        route = self.db.query(Route).filter(Route.id == route_id).first()
        if not route:
            raise ValueError(f"Route {route_id} not found")
        
        # Buscar pedidos da rota
        orders = self.db.query(Order).filter(
            Order.route_id == route_id,
            Order.operational_status == "delivered"
        ).all()
        
        if not orders:
            return {
                "route_id": route_id,
                "total_deliveries": 0,
                "total_payment": 0.0,
                "details": []
            }
        
        # Calcular pagamento para cada entrega
        payments = []
        total_payment = 0.0
        
        for order in orders:
            try:
                payment = self.calculate_delivery_payment(str(order.id))
                payments.append(payment)
                total_payment += payment["total_payment"]
            except Exception as e:
                print(f"Error calculating payment for order {order.id}: {e}")
        
        return {
            "route_id": route_id,
            "total_deliveries": len(orders),
            "total_distance_km": route.total_distance_km,
            "total_payment": round(total_payment, 2),
            "details": payments
        }
