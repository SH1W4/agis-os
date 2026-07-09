"""
Connectors for external platforms
"""
from src.ingestion.connectors.base import BaseConnector
from src.ingestion.connectors.manual import ManualConnector

__all__ = ['BaseConnector', 'ManualConnector']
