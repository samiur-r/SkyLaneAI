"""Alert generation routes"""
import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import Detection, EnrichedContext, CraftedMessage
from app.agents.message_agent import message_agent

logger = logging.getLogger(__name__)

router = APIRouter()


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
