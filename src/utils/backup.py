"""
Automated backup system for LogisticSmart.
"""
import os
import shutil
import gzip
import logging
from datetime import datetime
from pathlib import Path
from typing import List
import json

logger = logging.getLogger(__name__)


class BackupManager:
    """Manages automated backups of critical data."""
    
    def __init__(self, base_dir: Path = None):
        """
        Initialize backup manager.
        
        Args:
            base_dir: Base directory of the application
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent
        
        self.base_dir = base_dir
        self.backup_dir = base_dir / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_dir = base_dir / "data"
        self.reports_dir = base_dir / "Relatórios"
        self.logs_dir = base_dir / "logs"
    
    def create_backup(self, backup_name: str = None) -> Path:
        """
        Create a full backup of critical data.
        
        Args:
            backup_name: Custom name for the backup
            
        Returns:
            Path to the backup file
        """
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Backup database
            if self.data_dir.exists():
                db_backup = backup_path / "database"
                shutil.copytree(self.data_dir, db_backup)
                logger.info(f"Database backed up to {db_backup}")
            
            # Backup reports
            if self.reports_dir.exists():
                reports_backup = backup_path / "reports"
                shutil.copytree(self.reports_dir, reports_backup)
                logger.info(f"Reports backed up to {reports_backup}")
            
            # Backup logs (last 7 days only)
            if self.logs_dir.exists():
                logs_backup = backup_path / "logs"
                logs_backup.mkdir(parents=True, exist_ok=True)
                
                for log_file in self.logs_dir.glob("*.log"):
                    # Only copy recent logs
                    if log_file.stat().st_mtime > (datetime.now().timestamp() - 7 * 24 * 3600):
                        shutil.copy2(log_file, logs_backup / log_file.name)
                
                logger.info(f"Recent logs backed up to {logs_backup}")
            
            # Create backup metadata
            metadata = {
                "created_at": datetime.now().isoformat(),
                "backup_name": backup_name,
                "database_backed_up": self.data_dir.exists(),
                "reports_backed_up": self.reports_dir.exists(),
                "logs_backed_up": self.logs_dir.exists(),
                "total_size_mb": self._get_directory_size(backup_path) / (1024 * 1024)
            }
            
            with open(backup_path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Compress backup
            compressed_path = self._compress_backup(backup_path)
            
            # Remove uncompressed backup
            shutil.rmtree(backup_path)
            
            logger.info(f"Backup created successfully: {compressed_path}")
            return compressed_path
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            # Clean up failed backup
            if backup_path.exists():
                shutil.rmtree(backup_path)
            raise
    
    def _compress_backup(self, backup_path: Path) -> Path:
        """
        Compress backup directory to gzip.
        
        Args:
            backup_path: Path to backup directory
            
        Returns:
            Path to compressed backup
        """
        compressed_path = backup_path.parent / f"{backup_path.name}.tar.gz"
        
        # Create tar.gz archive
        shutil.make_archive(
            str(backup_path),
            'gztar',
            root_dir=backup_path.parent,
            base_dir=backup_path.name
        )
        
        return compressed_path
    
    def restore_backup(self, backup_file: Path) -> bool:
        """
        Restore from a backup file.
        
        Args:
            backup_file: Path to backup file (.tar.gz)
            
        Returns:
            True if successful
        """
        try:
            # Extract backup
            shutil.unpack_archive(str(backup_file), str(self.backup_dir))
            
            # Find extracted directory
            extracted_dir = self.backup_dir / backup_file.stem.replace('.tar', '')
            
            # Restore database
            if (extracted_dir / "database").exists():
                if self.data_dir.exists():
                    shutil.rmtree(self.data_dir)
                shutil.copytree(extracted_dir / "database", self.data_dir)
                logger.info("Database restored")
            
            # Restore reports
            if (extracted_dir / "reports").exists():
                if self.reports_dir.exists():
                    shutil.rmtree(self.reports_dir)
                shutil.copytree(extracted_dir / "reports", self.reports_dir)
                logger.info("Reports restored")
            
            # Restore logs
            if (extracted_dir / "logs").exists():
                if self.logs_dir.exists():
                    shutil.rmtree(self.logs_dir)
                shutil.copytree(extracted_dir / "logs", self.logs_dir)
                logger.info("Logs restored")
            
            # Clean up extracted directory
            shutil.rmtree(extracted_dir)
            
            logger.info(f"Backup restored successfully from {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def cleanup_old_backups(self, retention_days: int = 30) -> List[Path]:
        """
        Remove backups older than retention period.
        
        Args:
            retention_days: Number of days to keep backups
            
        Returns:
            List of removed backup paths
        """
        removed = []
        cutoff_time = datetime.now().timestamp() - (retention_days * 24 * 3600)
        
        for backup_file in self.backup_dir.glob("*.tar.gz"):
            if backup_file.stat().st_mtime < cutoff_time:
                backup_file.unlink()
                removed.append(backup_file)
                logger.info(f"Removed old backup: {backup_file}")
        
        return removed
    
    def list_backups(self) -> List[dict]:
        """
        List all available backups with metadata.
        
        Returns:
            List of backup information dictionaries
        """
        backups = []
        
        for backup_file in self.backup_dir.glob("*.tar.gz"):
            # Try to read metadata from compressed file
            metadata = {
                "file": str(backup_file),
                "size_mb": backup_file.stat().st_size / (1024 * 1024),
                "created": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat()
            }
            backups.append(metadata)
        
        return sorted(backups, key=lambda x: x["created"], reverse=True)
    
    def _get_directory_size(self, directory: Path) -> int:
        """
        Get total size of directory in bytes.
        
        Args:
            directory: Path to directory
            
        Returns:
            Size in bytes
        """
        total_size = 0
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
