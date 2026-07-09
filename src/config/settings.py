"""
Configurações centralizadas do LogisticSmart v3.0
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings

# Diretórios base
BASE_DIR = Path(__file__).parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "Relatórios"
TEMP_DIR = BASE_DIR / "temp"

# Configurações da aplicação
APP_CONFIG = {
    "name": "Agis",
    "version": "3.0.0",
    "description": "Agis Ops — Plataforma Cognitiva de Decisão e Operações Físicas",
    "author": "SH1W4",
    "max_upload_size": 200 * 1024 * 1024,  # 200MB
    "supported_formats": [".xlsx", ".xls", ".csv"],
}


class Settings(BaseSettings):
    """Configurações do Agis v3.0 usando Pydantic Settings"""
    
    # Application
    APP_NAME: str = "Agis"
    APP_VERSION: str = "3.0.0"
    APP_ENV: str = "development"
    
    # Database
    DATABASE_URL: str = "postgresql://agis:agis@localhost:5432/agis"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # External APIs
    SHOPPI_API_KEY: Optional[str] = None
    SHOPEE_API_KEY: Optional[str] = None
    WHATSAPP_API_KEY: Optional[str] = None
    
    # Sentry
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class FeatureFlags:
    """Feature flags para controle de funcionalidades"""
    ENABLE_OPERATIONAL_STATE: bool = True
    ENABLE_EVENT_SYSTEM: bool = True
    ENABLE_CELERY_WORKERS: bool = True
    ENABLE_JWT_AUTH: bool = True
    ENABLE_WEBHOOKS: bool = False  # Future
    ENABLE_LEARNING_ENGINE: bool = False  # Future


settings = Settings()
feature_flags = FeatureFlags()

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Agis Ops v3.0",
    "page_icon": "🧭",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Configurações de tema
THEME_CONFIG = {
    "base": "dark",
    "primaryColor": "#08c6ff",
    "backgroundColor": "#0f1116",
    "secondaryBackgroundColor": "#1c1f26",
    "textColor": "#f8f9fa",
}

# Configurações de cache
CACHE_CONFIG = {
    "ttl": 3600,  # 1 hora
    "max_entries": 100,
    "persist": True,
}

# Colunas obrigatórias e opcionais
REQUIRED_COLUMNS = ["Data prevista de entrega"]
OPTIONAL_COLUMNS = [
    "Entregador",
    "Cidade", 
    "Status",
    "Tipo de produto",
    "Destino",
    "Cliente",
    "Valor",
    "Observações"
]

# Filtros automáticos baseados em padrões
AUTO_FILTERS = {
    "status": ["Status", "Situação", "Estado"],
    "entregador": ["Entregador", "Responsável", "Motorista"],
    "cidade": ["Cidade", "Local", "Destino", "Município"],
    "produto": ["Produto", "Tipo de produto", "Item", "Mercadoria"],
    "cliente": ["Cliente", "Destinatário", "Receptor"],
}

# Configurações de exportação
EXPORT_CONFIG = {
    "excel": {
        "engine": "openpyxl",
        "index": False,
        "sheet_name": "Relatório",
    },
    "csv": {
        "index": False,
        "encoding": "utf-8-sig",
        "sep": ";"
    },
    "pdf": {
        "options": {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None
        }
    }
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": ["console", "file"],
    "file_path": BASE_DIR / "logs" / "agis.log",
}

def get_config(section: str = None) -> Dict[str, Any]:
    """
    Retorna configurações específicas ou todas as configurações.
    
    Args:
        section: Nome da seção de configuração
        
    Returns:
        Dicionário com as configurações
    """
    configs = {
        "app": APP_CONFIG,
        "streamlit": STREAMLIT_CONFIG,
        "theme": THEME_CONFIG,
        "cache": CACHE_CONFIG,
        "export": EXPORT_CONFIG,
        "logging": LOGGING_CONFIG,
    }
    
    if section:
        return configs.get(section, {})
    return configs

def create_directories():
    """Cria diretórios necessários se não existirem."""
    directories = [UPLOAD_DIR, REPORTS_DIR, TEMP_DIR, BASE_DIR / "logs"]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

