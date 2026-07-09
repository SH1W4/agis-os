"""
Script para executar o Celery worker
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workers.celery_app import celery_app

if __name__ == "__main__":
    celery_app.worker_main([
        'worker',
        '--loglevel=INFO',
        '--concurrency=4',
        '--pool=solo',  # Use 'prefork' in production
    ])
