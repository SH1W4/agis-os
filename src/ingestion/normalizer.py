"""
Order normalizer for LogisticSmart v3.0
Normalizes orders from different platforms to a standard format
"""
from typing import Dict, Any, Optional
from datetime import datetime
import re


class OrderNormalizer:
    """
    Normalizador de pedidos para formato padrão do LogisticSmart.
    
    Responsável por:
    1. Validar campos obrigatórios
    2. Padronizar formatos (telefone, CEP, etc.)
    3. Enriquecer dados quando possível
    4. Detectar e corrigir erros comuns
    """
    
    REQUIRED_FIELDS = [
        "address_street",
        "address_number",
        "address_city",
        "address_state",
        "address_zipcode"
    ]
    
    def __init__(self):
        """Inicializa o normalizador"""
        pass
    
    def normalize(self, raw_order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normaliza um pedido para o formato padrão.
        
        Args:
            raw_order: Pedido bruto de qualquer plataforma
            
        Returns:
            Pedido normalizado
        """
        normalized = {}
        
        # Mapear campos comuns
        normalized["origin_platform"] = raw_order.get("origin_platform", "manual")
        normalized["origin_order_id"] = raw_order.get("origin_order_id", "")
        
        # Endereço
        normalized["address_street"] = self._normalize_string(raw_order.get("address_street"))
        normalized["address_number"] = self._normalize_string(raw_order.get("address_number"))
        normalized["address_complement"] = self._normalize_string(raw_order.get("address_complement"))
        normalized["address_neighborhood"] = self._normalize_string(raw_order.get("address_neighborhood"))
        normalized["address_city"] = self._normalize_string(raw_order.get("address_city"))
        normalized["address_state"] = self._normalize_state(raw_order.get("address_state"))
        normalized["address_zipcode"] = self._normalize_zipcode(raw_order.get("address_zipcode"))
        
        # Coordenadas (se disponíveis)
        normalized["address_latitude"] = raw_order.get("address_latitude")
        normalized["address_longitude"] = raw_order.get("address_longitude")
        
        # Pacote
        normalized["weight_kg"] = self._normalize_float(raw_order.get("weight_kg"))
        normalized["length_cm"] = self._normalize_float(raw_order.get("length_cm"))
        normalized["width_cm"] = self._normalize_float(raw_order.get("width_cm"))
        normalized["height_cm"] = self._normalize_float(raw_order.get("height_cm"))
        normalized["volume_m3"] = self._calculate_volume(
            normalized["length_cm"],
            normalized["width_cm"],
            normalized["height_cm"]
        )
        
        # Financeiro
        normalized["declared_value_brl"] = self._normalize_float(raw_order.get("declared_value_brl"))
        normalized["shipping_cost_brl"] = self._normalize_float(raw_order.get("shipping_cost_brl"))
        
        # SLA
        normalized["promised_delivery_date"] = self._normalize_datetime(raw_order.get("promised_delivery_date"))
        normalized["priority"] = self._normalize_priority(raw_order.get("priority", "normal"))
        
        # Instruções
        normalized["special_instructions"] = self._normalize_string(raw_order.get("special_instructions"))
        
        # Metadados
        normalized["metadata"] = raw_order.get("metadata", {})
        
        return normalized
    
    def validate(self, order: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Valida se um pedido normalizado tem todos os campos obrigatórios.
        
        Args:
            order: Pedido normalizado
            
        Returns:
            (valid, error_message)
        """
        for field in self.REQUIRED_FIELDS:
            if not order.get(field):
                return False, f"Missing required field: {field}"
        
        # Validar CEP
        zipcode = order.get("address_zipcode")
        if zipcode and not self._is_valid_zipcode(zipcode):
            return False, f"Invalid zipcode format: {zipcode}"
        
        # Validar estado
        state = order.get("address_state")
        if state and not self._is_valid_state(state):
            return False, f"Invalid state code: {state}"
        
        return True, None
    
    def _normalize_string(self, value: Any) -> Optional[str]:
        """Normaliza string (remove espaços extras, converte para uppercase quando apropriado)"""
        if value is None:
            return None
        if isinstance(value, str):
            return value.strip()
        return str(value)
    
    def _normalize_float(self, value: Any) -> Optional[float]:
        """Normaliza valor float"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _normalize_datetime(self, value: Any) -> Optional[datetime]:
        """Normaliza datetime"""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        try:
            # Tenta parsear string ISO
            return datetime.fromisoformat(value)
        except (ValueError, TypeError):
            return None
    
    def _normalize_state(self, value: Any) -> Optional[str]:
        """Normaliza código de estado para 2 caracteres uppercase"""
        if value is None:
            return None
        state = str(value).strip().upper()
        # Se tiver mais de 2 caracteres, tenta pegar os primeiros 2
        if len(state) > 2:
            state = state[:2]
        return state
    
    def _normalize_zipcode(self, value: Any) -> Optional[str]:
        """Normaliza CEP (remove caracteres não numéricos)"""
        if value is None:
            return None
        # Remove tudo que não é dígito
        zipcode = re.sub(r'\D', '', str(value))
        # CEP brasileiro tem 8 dígitos
        if len(zipcode) == 8:
            return zipcode
        return zipcode
    
    def _calculate_volume(self, length: Optional[float], width: Optional[float], height: Optional[float]) -> Optional[float]:
        """Calcula volume em m³ a partir de dimensões em cm"""
        if length and width and height:
            # Converter cm³ para m³
            volume_cm3 = length * width * height
            return volume_cm3 / 1_000_000
        return None
    
    def _normalize_priority(self, value: Any) -> str:
        """Normaliza prioridade"""
        if value is None:
            return "normal"
        priority = str(value).lower()
        valid_priorities = ["low", "normal", "high", "urgent"]
        if priority in valid_priorities:
            return priority
        return "normal"
    
    def _is_valid_zipcode(self, zipcode: str) -> bool:
        """Valida formato de CEP brasileiro"""
        if not zipcode:
            return False
        # CEP deve ter 8 dígitos
        return len(zipcode) == 8 and zipcode.isdigit()
    
    def _is_valid_state(self, state: str) -> bool:
        """Valida código de estado brasileiro"""
        valid_states = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        return state.upper() in valid_states
