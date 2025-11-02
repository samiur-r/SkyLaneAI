"""Alert generation routes"""
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.models.schemas import (
    Detection,
    EnrichedContext,
    CraftedMessage,
    ActionRecommendation,
    NaturalLanguageAlert
)
from app.agents.message_agent import message_agent
from app.agents.action_agent import action_agent
from app.workflows.alert_workflow import alert_workflow

logger = logging.getLogger(__name__)

router = APIRouter()


class BatchDetectionRequest(BaseModel):
    """Request model for batch alert generation"""
    detections: List[Detection]
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    return_top_n: Optional[int] = None


@router.post("/generate-message", response_model=CraftedMessage)
async def generate_alert_message(detection: Detection, context: EnrichedContext):
    """
    Generate a natural language alert message for a detection

    Args:
        detection: Detection data
        context: Enriched context

    Returns:
        CraftedMessage with title, emoji, body, and sections
    """
    try:
        message = await message_agent.craft_message(detection, context)
        return message
    except Exception as e:
        logger.error(f"Error generating alert message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate message: {str(e)}"
        )


@router.post("/generate-action", response_model=ActionRecommendation)
async def generate_action_recommendation(detection: Detection, context: EnrichedContext):
    """
    Generate action recommendations for a detection

    Args:
        detection: Detection data
        context: Enriched context

    Returns:
        ActionRecommendation with primary/secondary actions and urgency
    """
    try:
        action = await action_agent.recommend_action(detection, context)
        return action
    except Exception as e:
        logger.error(f"Error generating action recommendation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate action: {str(e)}"
        )


@router.post("/generate-complete", response_model=NaturalLanguageAlert)
async def generate_complete_alert(
    detection: Detection,
    image_width: Optional[int] = Query(None),
    image_height: Optional[int] = Query(None)
):
    """
    Generate a complete alert using all 4 agents (context, message, action, priority)

    Args:
        detection: Detection data
        image_width: Video/image width in pixels
        image_height: Video/image height in pixels

    Returns:
        Complete NaturalLanguageAlert with all components
    """
    try:
        alert = await alert_workflow.generate_complete_alert(
            detection,
            image_width,
            image_height
        )
        return alert
    except Exception as e:
        logger.error(f"Error generating complete alert: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate alert: {str(e)}"
        )


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
