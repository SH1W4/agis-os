"""
Base connector for external platforms
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime


class BaseConnector(ABC):
    """
    Classe base para conectores de plataformas externas.
    
    Cada plataforma (Shoppi, Shopee, Mercado Livre, etc.) deve
    implementar esta classe para fornecer dados padronizados.
    """
    
    def __init__(self, api_key: str = None):
        """
        Inicializa o conector.
        
        Args:
            api_key: Chave de API da plataforma (opcional)
        """
        self.api_key = api_key
    
    @abstractmethod
    def fetch_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Busca pedidos da plataforma em um intervalo de datas.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            
        Returns:
            Lista de pedidos em formato bruto
        """
        pass
    
    @abstractmethod
    def normalize_order(self, raw_order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normaliza um pedido bruto para o formato padrão do LogisticSmart.
        
        Args:
            raw_order: Pedido em formato bruto da plataforma
            
        Returns:
            Pedido normalizado
        """
        pass
    
    @abstractmethod
    def validate_webhook(self, payload: Dict[str, Any], signature: str) -> bool:
        """
        Valida um webhook recebido da plataforma.
        
        Args:
            payload: Payload do webhook
            signature: Assinatura do webhook
            
        Returns:
            True se válido, False caso contrário
        """
        pass
    
    def get_platform_name(self) -> str:
        """
        Retorna o nome da plataforma.
        
        Returns:
            Nome da plataforma
        """
        return self.__class__.__name__.replace("Connector", "").lower()
