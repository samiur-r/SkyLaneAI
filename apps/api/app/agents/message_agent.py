"""Message Crafting Agent - LLM-powered message generation"""
import logging
import re
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.models.schemas import Detection, EnrichedContext, CraftedMessage
from app.core.config import settings

logger = logging.getLogger(__name__)


class MessageCraftingAgent:
    """
    LLM-powered agent that generates human-readable alert messages.
    Uses GPT-5-nano for natural language generation.
    """

    # Emoji mapping for different hazard types
    HAZARD_EMOJIS = {
        "bird": "🦅",
        "drone": "🚁",
        "balloon": "🎈",
        "kite": "🪁",
        "airplane": "✈️",
        "sports ball": "⚽",  # May be balloons
        "default": "⚠️"
    }

    def __init__(self):
        """Initialize the Message Crafting Agent"""
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set. Message crafting will fail.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0.3,  # Some creativity but mostly consistent
                timeout=settings.ALERT_GENERATION_TIMEOUT,
                api_key=settings.OPENAI_API_KEY
            )
            logger.info(f"MessageCraftingAgent initialized with model: {settings.OPENAI_MODEL}")

    def _get_emoji(self, class_name: str) -> str:
        """Get appropriate emoji for hazard type"""
        return self.HAZARD_EMOJIS.get(class_name.lower(), self.HAZARD_EMOJIS["default"])

    async def craft_message(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> CraftedMessage:
        """
        Generate a human-readable alert message from detection and context

        Args:
            detection: The detection data
            context: Enriched context from Context Agent

        Returns:
            CraftedMessage with title, emoji, body, and parsed sections
        """
        if not self.llm:
            raise RuntimeError("LLM not initialized. Please set OPENAI_API_KEY.")

        try:
            # Build the prompt
            system_prompt = """You are an aviation safety expert communicating to flying taxi pilots.
Your job is to create clear, concise, and actionable alert messages about detected hazards.

Guidelines:
- Be direct and professional
- Use aviation terminology appropriately
- Keep the message scannable (use bullet points and sections)
- Focus on what the pilot needs to know immediately
- Use markdown formatting for structure
- Do NOT include emojis (they will be added separately)
- Keep total message under 200 words"""

            user_prompt = f"""Generate a safety alert message for this detection:

Object Details:
- Type: {detection.class_name}
- Confidence: {detection.confidence:.0%}
- Timestamp: {detection.timestamp:.1f}s (Frame {detection.frame_number})

Contextual Analysis:
- Size Category: {context.estimated_size}
- Screen Position: {context.screen_position}
- Bounding Box Area: {context.bbox_area_pixels:,} pixels²
- Initial Threat Level: {context.threat_level_raw}

Create a structured alert message with:
1. A clear title (e.g., "Large Bird Detection" or "Drone Hazard Detected")
2. Detection Details section (time, location, confidence)
3. Threat Assessment section (size, position, initial analysis)

Use this exact format:
# [Title]

**Detection Details:**
- [bullet points]

**Threat Assessment:**
- [bullet points]

Keep it brief and actionable. No fluff."""

            # Call LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = await self.llm.ainvoke(messages)
            message_body = response.content

            # Extract title and parse sections
            title = self._extract_title(message_body, detection.class_name)
            emoji = self._get_emoji(detection.class_name)
            sections = self._parse_sections(message_body)

            crafted_message = CraftedMessage(
                title=title,
                emoji=emoji,
                body=message_body,
                sections=sections
            )

            logger.debug(f"Crafted message for {detection.class_name}: {title}")
            return crafted_message

        except Exception as e:
            logger.error(f"Error crafting message: {e}")
            # Return fallback message
            return self._create_fallback_message(detection, context)

    def _extract_title(self, message_body: str, class_name: str) -> str:
        """Extract title from the message body"""
        # Look for markdown heading
        match = re.search(r'^#\s+(.+)$', message_body, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Look for first line if it looks like a title
        lines = message_body.strip().split('\n')
        if lines:
            first_line = lines[0].strip('# ').strip()
            if len(first_line) < 50:  # Reasonable title length
                return first_line

        # Fallback to generated title
        return f"{class_name.title()} Detection"

    def _parse_sections(self, message_body: str) -> dict:
        """Parse the message body into sections"""
        sections = {}

        # Extract Detection Details section
        detection_match = re.search(
            r'\*\*Detection Details:\*\*(.*?)(?=\*\*|$)',
            message_body,
            re.DOTALL
        )
        if detection_match:
            sections["detection_details"] = detection_match.group(1).strip()

        # Extract Threat Assessment section
        threat_match = re.search(
            r'\*\*Threat Assessment:\*\*(.*?)(?=\*\*|$)',
            message_body,
            re.DOTALL
        )
        if threat_match:
            sections["threat_assessment"] = threat_match.group(1).strip()

        return sections

    def _create_fallback_message(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> CraftedMessage:
        """Create a fallback message if LLM fails"""
        title = f"{detection.class_name.title()} Detection"
        emoji = self._get_emoji(detection.class_name)

        body = f"""# {title}

**Detection Details:**
- Detected at {detection.timestamp:.1f} seconds
- Position: {context.screen_position}
- Confidence: {detection.confidence:.0%}

**Threat Assessment:**
- Size: {context.estimated_size.title()}
- Area: {context.bbox_area_pixels:,} pixels²
- Initial Threat Level: {context.threat_level_raw.title()}

Monitor this hazard and maintain safe distance."""

        sections = {
            "detection_details": f"Detected at {detection.timestamp:.1f}s",
            "threat_assessment": f"Threat level: {context.threat_level_raw}"
        }

        return CraftedMessage(
            title=title,
            emoji=emoji,
            body=body,
            sections=sections
        )


# Global instance
message_agent = MessageCraftingAgent()
