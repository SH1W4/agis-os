"""
Audit logging system for tracking user actions.
"""
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database.models import AuditLog
from src.database.session import get_db_context

logger = logging.getLogger(__name__)


class AuditLogger:
    """Logger for auditing user actions."""
    
    def __init__(self):
        """Initialize audit logger."""
        self.logger = logging.getLogger("logistic_smart.audit")
    
    def log_action(
        self,
        user_id: int,
        action: str,
        resource_type: str = None,
        resource_id: int = None,
        details: Dict[str, Any] = None,
        ip_address: str = None,
        user_agent: str = None
    ) -> AuditLog:
        """
        Log a user action to the database.
        
        Args:
            user_id: ID of the user performing the action
            action: Action performed (login, upload, export, delete, etc.)
            resource_type: Type of resource affected (delivery, report, user)
            resource_id: ID of the resource affected
            details: Additional details about the action
            ip_address: IP address of the user
            user_agent: User agent string
            
        Returns:
            Created AuditLog entry
        """
        try:
            with get_db_context() as db:
                audit_entry = AuditLog(
                    user_id=user_id,
                    action=action,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    details=details or {},
                    ip_address=ip_address,
                    user_agent=user_agent,
                    created_at=datetime.utcnow()
                )
                
                db.add(audit_entry)
                db.flush()
                
                # Also log to file for immediate visibility
                self.logger.info(
                    f"User {user_id} performed action: {action} "
                    f"on {resource_type}:{resource_id}"
                )
                
                return audit_entry
                
        except Exception as e:
            logger.error(f"Failed to log audit entry: {e}")
            # Don't raise - audit failures shouldn't break the application
            return None
    
    def log_login(self, user_id: int, ip_address: str = None, user_agent: str = None):
        """Log user login."""
        return self.log_action(
            user_id=user_id,
            action="login",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_logout(self, user_id: int, ip_address: str = None):
        """Log user logout."""
        return self.log_action(
            user_id=user_id,
            action="logout",
            ip_address=ip_address
        )
    
    def log_file_upload(
        self,
        user_id: int,
        file_name: str,
        record_count: int,
        ip_address: str = None
    ):
        """Log file upload."""
        return self.log_action(
            user_id=user_id,
            action="upload",
            resource_type="delivery",
            details={
                "file_name": file_name,
                "record_count": record_count
            },
            ip_address=ip_address
        )
    
    def log_report_export(
        self,
        user_id: int,
        report_type: str,
        delivery_id: int,
        record_count: int,
        ip_address: str = None
    ):
        """Log report export."""
        return self.log_action(
            user_id=user_id,
            action="export",
            resource_type="report",
            resource_id=delivery_id,
            details={
                "report_type": report_type,
                "record_count": record_count
            },
            ip_address=ip_address
        )
    
    def log_user_creation(
        self,
        admin_id: int,
        new_user_id: int,
        username: str,
        role: str
    ):
        """Log user creation."""
        return self.log_action(
            user_id=admin_id,
            action="create_user",
            resource_type="user",
            resource_id=new_user_id,
            details={
                "username": username,
                "role": role
            }
        )
    
    def log_user_deletion(
        self,
        admin_id: int,
        deleted_user_id: int,
        username: str
    ):
        """Log user deletion."""
        return self.log_action(
            user_id=admin_id,
            action="delete_user",
            resource_type="user",
            resource_id=deleted_user_id,
            details={
                "username": username
            }
        )
    
    def get_user_audit_trail(
        self,
        user_id: int,
        limit: int = 100
    ) -> list:
        """
        Get audit trail for a specific user.
        
        Args:
            user_id: ID of the user
            limit: Maximum number of entries to return
            
        Returns:
            List of audit log entries
        """
        try:
            with get_db_context() as db:
                entries = db.query(AuditLog).filter(
                    AuditLog.user_id == user_id
                ).order_by(
                    AuditLog.created_at.desc()
                ).limit(limit).all()
                
                return entries
                
        except Exception as e:
            logger.error(f"Failed to get audit trail: {e}")
            return []
    
    def get_resource_history(
        self,
        resource_type: str,
        resource_id: int,
        limit: int = 50
    ) -> list:
        """
        Get history for a specific resource.
        
        Args:
            resource_type: Type of resource
            resource_id: ID of the resource
            limit: Maximum number of entries to return
            
        Returns:
            List of audit log entries
        """
        try:
            with get_db_context() as db:
                entries = db.query(AuditLog).filter(
                    AuditLog.resource_type == resource_type,
                    AuditLog.resource_id == resource_id
                ).order_by(
                    AuditLog.created_at.desc()
                ).limit(limit).all()
                
                return entries
                
        except Exception as e:
            logger.error(f"Failed to get resource history: {e}")
            return []


# Global audit logger instance
audit_logger = AuditLogger()
