"""
Action Recommendation Agent
Suggests pilot actions based on detection and context using LLM.
"""

import asyncio
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.models.schemas import Detection, EnrichedContext, ActionRecommendation


class ActionRecommendationAgent:
    """
    LLM-powered agent that provides actionable recommendations for pilots.

    This agent analyzes the hazard type, context, and threat level to suggest
    specific actions the pilot should take, following aviation safety protocols.
    """

    def __init__(self):
        """Initialize the Action Recommendation Agent with LLM."""
        if not settings.OPENAI_API_KEY:
            print("WARNING: OPENAI_API_KEY not set. Action recommendations will use fallback logic.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0.2,  # Low temperature for consistent, safe recommendations
                timeout=settings.ALERT_GENERATION_TIMEOUT,
                api_key=settings.OPENAI_API_KEY
            )

    async def recommend_action(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> ActionRecommendation:
        """
        Generate action recommendations based on detection and context.

        Args:
            detection: The hazard detection data
            context: Enriched context information

        Returns:
            ActionRecommendation with primary and secondary actions
        """
        # If LLM is not available, use fallback
        if self.llm is None:
            return self._create_fallback_action(detection, context)

        try:
            # Build the prompt
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(detection, context)

            # Call LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = await asyncio.wait_for(
                self.llm.ainvoke(messages),
                timeout=settings.ALERT_GENERATION_TIMEOUT
            )

            # Parse the response
            action_recommendation = self._parse_response(
                response.content,
                detection,
                context
            )

            return action_recommendation

        except asyncio.TimeoutError:
            print(f"Action recommendation timed out for {detection.class_name}")
            return self._create_fallback_action(detection, context)
        except Exception as e:
            print(f"Error generating action recommendation: {e}")
            return self._create_fallback_action(detection, context)

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the LLM."""
        return """You are an aviation safety expert AI assistant for SkyLaneAI, a collision avoidance system for flying taxis and aerial vehicles.

Your role is to provide ACTIONABLE, SPECIFIC recommendations for pilots when hazards are detected.

Guidelines:
1. PRIMARY ACTION: The most critical, immediate action (imperative, concise)
2. SECONDARY ACTION: Follow-up or alternative action (imperative, concise)
3. REASONING: Brief explanation of why these actions are recommended (1-2 sentences)
4. Use aviation terminology appropriately
5. Consider the threat level, hazard type, and position
6. Prioritize safety and collision avoidance
7. Be direct and clear - pilots need quick decisions

Response format:
PRIMARY: [imperative action]
SECONDARY: [imperative action]
REASONING: [brief explanation]

Example:
PRIMARY: Maintain current altitude and reduce speed to 40 knots
SECONDARY: Monitor hazard movement and prepare for evasive ascent if distance decreases
REASONING: The large bird detected in the center screen at moderate threat level requires cautious monitoring without aggressive maneuvers that could startle the bird or destabilize the aircraft."""

    def _build_user_prompt(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> str:
        """Build the user prompt with detection details."""
        return f"""Hazard Detection:
- Type: {detection.class_name}
- Confidence: {detection.confidence:.1%}
- Threat Level: {context.threat_level_raw}
- Size: {context.estimated_size}
- Position: {context.screen_position}
- Screen Coverage: {context.bbox_area_pixels} pixels

Provide action recommendations for the pilot."""

    def _parse_response(
        self,
        response_text: str,
        detection: Detection,
        context: EnrichedContext
    ) -> ActionRecommendation:
        """Parse LLM response into ActionRecommendation structure."""
        lines = response_text.strip().split('\n')

        primary_action = ""
        secondary_action = ""
        reasoning = ""

        for line in lines:
            line = line.strip()
            if line.startswith("PRIMARY:"):
                primary_action = line.replace("PRIMARY:", "").strip()
            elif line.startswith("SECONDARY:"):
                secondary_action = line.replace("SECONDARY:", "").strip()
            elif line.startswith("REASONING:"):
                reasoning = line.replace("REASONING:", "").strip()

        # Fallback if parsing failed
        if not primary_action:
            return self._create_fallback_action(detection, context)

        # Determine urgency from threat level
        urgency = self._determine_urgency(context.threat_level_raw)

        return ActionRecommendation(
            primary_action=primary_action,
            secondary_action=secondary_action or "Continue monitoring hazard trajectory",
            reasoning=reasoning or "Standard collision avoidance protocol",
            urgency=urgency
        )

    def _determine_urgency(self, threat_level: str) -> str:
        """Map threat level to urgency."""
        threat_to_urgency = {
            "critical": "immediate",
            "high": "urgent",
            "moderate": "caution",
            "low": "advisory"
        }
        return threat_to_urgency.get(threat_level.lower(), "advisory")

    def _create_fallback_action(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> ActionRecommendation:
        """
        Create rule-based action recommendations as fallback.

        This is used when LLM fails or times out.
        """
        threat_level = context.threat_level_raw.lower()
        hazard_type = detection.class_name.lower()
        position = context.screen_position.lower()
        size = context.estimated_size.lower()

        # Rule-based recommendations
        if threat_level == "critical":
            if "center" in position:
                primary = "Execute immediate evasive maneuver - ascend or bank right"
                secondary = "Alert air traffic control and activate collision warning"
            else:
                primary = "Reduce speed immediately and monitor hazard closely"
                secondary = "Prepare for evasive action if hazard moves toward center"
            reasoning = f"Critical threat level requires immediate defensive action to avoid collision with {hazard_type}."
            urgency = "immediate"

        elif threat_level == "high":
            if size == "large":
                primary = "Reduce speed to 40 knots and maintain current altitude"
                secondary = "Monitor hazard trajectory and prepare evasive ascent"
            else:
                primary = "Adjust course 10 degrees to avoid hazard path"
                secondary = "Maintain vigilant monitoring of hazard position"
            reasoning = f"High threat from {size} {hazard_type} requires cautious maneuvering."
            urgency = "urgent"

        elif threat_level == "moderate":
            primary = f"Maintain awareness of {hazard_type} position"
            secondary = "Slight course adjustment if hazard moves toward flight path"
            reasoning = f"Moderate threat requires monitoring without aggressive maneuvers."
            urgency = "caution"

        else:  # low
            primary = f"Continue current flight path, monitor {hazard_type}"
            secondary = "No immediate action required, maintain standard vigilance"
            reasoning = f"Low threat level - {hazard_type} is distant and not on collision course."
            urgency = "advisory"

        return ActionRecommendation(
            primary_action=primary,
            secondary_action=secondary,
            reasoning=reasoning,
            urgency=urgency
        )


# Singleton instance
action_agent = ActionRecommendationAgent()
