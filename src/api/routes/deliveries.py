"""
Delivery data routes for API.
"""
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.models import Delivery
from src.database.session import get_db_context
from src.utils.data_processor import DataProcessor

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


class DeliveryResponse(BaseModel):
    """Delivery response model."""
    id: int
    file_name: str
    total_records: int
    status: str
    uploaded_at: str
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[DeliveryResponse])
async def list_deliveries(skip: int = 0, limit: int = 100):
    """
    List all deliveries.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of deliveries
    """
    try:
        with get_db_context() as db:
            deliveries = db.query(Delivery).offset(skip).limit(limit).all()
            return deliveries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(delivery_id: int):
    """
    Get specific delivery by ID.
    
    Args:
        delivery_id: Delivery ID
        
    Returns:
        Delivery details
    """
    try:
        with get_db_context() as db:
            delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
            
            if not delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery not found"
                )
            
            return delivery
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/upload")
async def upload_delivery_file(file: UploadFile = File(...)):
    """
    Upload delivery data file.
    
    Args:
        file: Uploaded file
        
    Returns:
        Upload status and delivery ID
    """
    try:
        processor = DataProcessor()
        
        # Read file content
        content = await file.read()
        
        # Process file
        success, message, df = processor.load_file(content, file.filename)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Save to database
        with get_db_context() as db:
            delivery = Delivery(
                file_name=file.filename,
                file_size=len(content),
                total_records=len(df),
                status='completed',
                processed_records=len(df),
                detected_columns=processor.detected_columns
            )
            
            db.add(delivery)
            db.flush()
            
            return {
                "success": True,
                "delivery_id": delivery.id,
                "message": message,
                "records_processed": len(df)
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{delivery_id}")
async def delete_delivery(delivery_id: int):
    """
    Delete a delivery.
    
    Args:
        delivery_id: Delivery ID
        
    Returns:
        Deletion status
    """
    try:
        with get_db_context() as db:
            delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
            
            if not delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery not found"
                )
            
            db.delete(delivery)
            
            return {
                "success": True,
                "message": "Delivery deleted successfully"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
