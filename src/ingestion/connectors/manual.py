"""
Manual connector for manually entered orders
"""
from typing import Dict, Any, List
from datetime import datetime
from .base import BaseConnector


class ManualConnector(BaseConnector):
    """
    Conector para pedidos inseridos manualmente.
    Usado para pedidos que não vêm de plataformas externas.
    """
    
    def fetch_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Não aplicável para conector manual.
        
        Returns:
            Lista vazia
        """
        return []
    
    def normalize_order(self, raw_order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retorna o pedido como está, já deve estar no formato correto.
        
        Args:
            raw_order: Pedido manual
            
        Returns:
            Pedido normalizado (mesmo objeto)
        """
        return raw_order
    
    def validate_webhook(self, payload: Dict[str, Any], signature: str) -> bool:
        """
        Não aplicável para conector manual.
        
        Returns:
            False
        """
        return False
    
    def create_manual_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um pedido manual com validação básica.
        
        Args:
            order_data: Dados do pedido manual
            
        Returns:
            Pedido normalizado
        """
        # Adiciona metadados de origem manual
        normalized = {
            "origin_platform": "manual",
            "origin_order_id": f"MANUAL-{datetime.utcnow().timestamp()}",
            **order_data
        }
        
        return self.normalize_order(normalized)
