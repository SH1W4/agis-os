"""
Script de migração de SQLite para PostgreSQL
Migra dados do LogisticSmart v2.0 (SQLite) para v3.0 (PostgreSQL)
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_sqlite_to_postgres():
    """
    Migra dados do SQLite para PostgreSQL.
    
    Tabelas migradas:
    - users
    - deliveries
    - reports
    - audit_logs
    
    Novas tabelas (v3.0) não precisam de migração:
    - deposits
    - customers
    - drivers
    - orders
    - routes
    - operational_events
    - operational_states
    """
    
    # SQLite connection (v2.0)
    sqlite_db_path = Path(__file__).parent.parent / "data" / "logistic_smart.db"
    sqlite_url = f"sqlite:///{sqlite_db_path}"
    
    logger.info(f"Conectando ao SQLite: {sqlite_db_path}")
    sqlite_engine = create_engine(sqlite_url)
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    sqlite_session = SQLiteSession()
    
    # PostgreSQL connection (v3.0)
    logger.info(f"Conectando ao PostgreSQL: {settings.DATABASE_URL}")
    postgres_engine = create_engine(settings.DATABASE_URL)
    PostgresSession = sessionmaker(bind=postgres_engine)
    postgres_session = PostgresSession()
    
    try:
        # Migrar Users
        logger.info("Migrando users...")
        migrate_users(sqlite_session, postgres_session)
        
        # Migrar Deliveries
        logger.info("Migrando deliveries...")
        migrate_deliveries(sqlite_session, postgres_session)
        
        # Migrar Reports
        logger.info("Migrando reports...")
        migrate_reports(sqlite_session, postgres_session)
        
        # Migrar AuditLogs
        logger.info("Migrando audit_logs...")
        migrate_audit_logs(sqlite_session, postgres_session)
        
        logger.info("Migração concluída com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante migração: {e}")
        postgres_session.rollback()
        raise
    
    finally:
        sqlite_session.close()
        postgres_session.close()
        sqlite_engine.dispose()
        postgres_engine.dispose()


def migrate_users(sqlite_session, postgres_session):
    """Migra tabela users"""
    from src.database.models import User
    
    # Ler do SQLite
    sqlite_users = sqlite_session.execute(text("SELECT * FROM users")).fetchall()
    
    for user_data in sqlite_users:
        user_dict = {
            'username': user_data[1],
            'email': user_data[2],
            'password_hash': user_data[3],
            'name': user_data[4],
            'role': user_data[5],
            'active': user_data[6],
            'two_factor_enabled': user_data[7],
            'two_factor_secret': user_data[8],
            'created_at': user_data[9],
            'updated_at': user_data[10],
            'last_login': user_data[11],
        }
        
        # Criar no PostgreSQL
        postgres_user = User(**user_dict)
        postgres_session.add(postgres_user)
    
    postgres_session.commit()
    logger.info(f"Migrados {len(sqlite_users)} users")


def migrate_deliveries(sqlite_session, postgres_session):
    """Migra tabela deliveries"""
    from src.database.models import Delivery
    
    sqlite_deliveries = sqlite_session.execute(text("SELECT * FROM deliveries")).fetchall()
    
    for delivery_data in sqlite_deliveries:
        delivery_dict = {
            'file_name': delivery_data[1],
            'file_path': delivery_data[2],
            'file_size': delivery_data[3],
            'total_records': delivery_data[4],
            'processed_records': delivery_data[5],
            'status': delivery_data[6],
            'error_message': delivery_data[7],
            'detected_columns': delivery_data[8],
            'uploaded_by': delivery_data[9],
            'uploaded_at': delivery_data[10],
            'processed_at': delivery_data[11],
        }
        
        postgres_delivery = Delivery(**delivery_dict)
        postgres_session.add(postgres_delivery)
    
    postgres_session.commit()
    logger.info(f"Migrados {len(sqlite_deliveries)} deliveries")


def migrate_reports(sqlite_session, postgres_session):
    """Migra tabela reports"""
    from src.database.models import Report
    
    sqlite_reports = sqlite_session.execute(text("SELECT * FROM reports")).fetchall()
    
    for report_data in sqlite_reports:
        report_dict = {
            'delivery_id': report_data[1],
            'report_type': report_data[2],
            'file_path': report_data[3],
            'file_size': report_data[4],
            'filters_used': report_data[5],
            'total_deliveries': report_data[6],
            'unique_deliverers': report_data[7],
            'date_range_start': report_data[8],
            'date_range_end': report_data[9],
            'generated_by': report_data[10],
            'generated_at': report_data[11],
        }
        
        postgres_report = Report(**report_dict)
        postgres_session.add(postgres_report)
    
    postgres_session.commit()
    logger.info(f"Migrados {len(sqlite_reports)} reports")


def migrate_audit_logs(sqlite_session, postgres_session):
    """Migra tabela audit_logs"""
    from src.database.models import AuditLog
    
    sqlite_audit_logs = sqlite_session.execute(text("SELECT * FROM audit_logs")).fetchall()
    
    for audit_data in sqlite_audit_logs:
        audit_dict = {
            'user_id': audit_data[1],
            'action': audit_data[2],
            'resource_type': audit_data[3],
            'resource_id': str(audit_data[4]) if audit_data[4] else None,  # Convert to string
            'details': audit_data[5],
            'ip_address': audit_data[6],
            'user_agent': audit_data[7],
            'created_at': audit_data[8],
        }
        
        postgres_audit = AuditLog(**audit_dict)
        postgres_session.add(postgres_audit)
    
    postgres_session.commit()
    logger.info(f"Migrados {len(sqlite_audit_logs)} audit_logs")


if __name__ == "__main__":
    logger.info("Iniciando migração SQLite -> PostgreSQL")
    migrate_sqlite_to_postgres()
