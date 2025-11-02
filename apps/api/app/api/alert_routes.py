"""Alert generation routes"""
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.schemas import (
    Detection,
    NaturalLanguageAlert
)
from app.workflows.alert_workflow import alert_workflow

logger = logging.getLogger(__name__)

router = APIRouter()


class BatchDetectionRequest(BaseModel):
    """Request model for batch alert generation"""
    detections: List[Detection]
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    return_top_n: Optional[int] = None


@router.post("/generate-batch", response_model=List[NaturalLanguageAlert])
async def generate_batch_alerts(request: BatchDetectionRequest):
    """
    Generate complete alerts for multiple detections

    Args:
        request: Batch request with detections and optional parameters

    Returns:
        List of NaturalLanguageAlerts sorted by priority (highest first)
    """
    try:
        alerts = await alert_workflow.generate_batch_alerts(
            request.detections,
            request.image_width,
            request.image_height,
            request.return_top_n
        )
        return alerts
    except Exception as e:
        logger.error(f"Error generating batch alerts: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate batch alerts: {str(e)}"
        )


@router.post("/generate-summary")
async def generate_summary_report(request: BatchDetectionRequest):
    """
    Generate a summary report with analytics for all detections

    Args:
        request: Batch request with detections

    Returns:
        Summary report with statistics and top alerts
    """
    try:
        summary = await alert_workflow.generate_summary_report(
            request.detections,
            request.image_width,
            request.image_height
        )
        return summary
    except Exception as e:
        logger.error(f"Error generating summary report: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}"
        )
