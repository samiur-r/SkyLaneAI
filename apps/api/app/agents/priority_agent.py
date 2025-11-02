"""
Priority Scoring Agent
Calculates priority scores for alerts using rule-based logic.
"""

from typing import List, Tuple
from app.models.schemas import (
    Detection,
    EnrichedContext,
    ActionRecommendation,
    PriorityScore
)


class PriorityScoringAgent:
    """
    Rule-based agent that calculates priority scores for hazard alerts.

    This agent uses a weighted scoring system to rank alerts by urgency,
    helping pilots focus on the most critical threats first.

    Scoring factors:
    - Threat level (40%): critical > high > moderate > low
    - Action urgency (30%): immediate > urgent > caution > advisory
    - Confidence (20%): Higher confidence = higher priority
    - Size (10%): Larger hazards = higher priority
    """

    # Weight configuration
    WEIGHTS = {
        "threat_level": 0.40,
        "action_urgency": 0.30,
        "confidence": 0.20,
        "size": 0.10
    }

    # Scoring maps
    THREAT_SCORES = {
        "critical": 100,
        "high": 75,
        "moderate": 50,
        "low": 25
    }

    URGENCY_SCORES = {
        "immediate": 100,
        "urgent": 75,
        "caution": 50,
        "advisory": 25
    }

    SIZE_SCORES = {
        "large": 100,
        "medium": 60,
        "small": 30
    }

    def calculate_priority(
        self,
        detection: Detection,
        context: EnrichedContext,
        action: ActionRecommendation
    ) -> PriorityScore:
        """
        Calculate priority score for an alert.

        Args:
            detection: The hazard detection
            context: Enriched context
            action: Action recommendation

        Returns:
            PriorityScore with overall score and breakdown
        """
        # Calculate component scores
        threat_score = self._score_threat_level(context.threat_level_raw)
        urgency_score = self._score_urgency(action.urgency)
        confidence_score = self._score_confidence(detection.confidence)
        size_score = self._score_size(context.estimated_size)

        # Calculate weighted total (0-100 scale)
        total_score = (
            threat_score * self.WEIGHTS["threat_level"] +
            urgency_score * self.WEIGHTS["action_urgency"] +
            confidence_score * self.WEIGHTS["confidence"] +
            size_score * self.WEIGHTS["size"]
        )

        # Determine priority level
        priority_level = self._determine_priority_level(total_score)

        # Build factors breakdown
        factors = {
            "threat_level": {
                "value": context.threat_level_raw,
                "score": round(threat_score, 1),
                "weight": self.WEIGHTS["threat_level"]
            },
            "action_urgency": {
                "value": action.urgency,
                "score": round(urgency_score, 1),
                "weight": self.WEIGHTS["action_urgency"]
            },
            "confidence": {
                "value": f"{detection.confidence:.1%}",
                "score": round(confidence_score, 1),
                "weight": self.WEIGHTS["confidence"]
            },
            "size": {
                "value": context.estimated_size,
                "score": round(size_score, 1),
                "weight": self.WEIGHTS["size"]
            }
        }

        return PriorityScore(
            overall_score=round(total_score, 2),
            priority_level=priority_level,
            factors=factors
        )

    def rank_alerts(
        self,
        alerts: List[Tuple[Detection, EnrichedContext, ActionRecommendation]]
    ) -> List[Tuple[Detection, EnrichedContext, ActionRecommendation, PriorityScore]]:
        """
        Calculate priority scores for multiple alerts and rank them.

        Args:
            alerts: List of (detection, context, action) tuples

        Returns:
            Sorted list of (detection, context, action, priority) tuples
            (highest priority first)
        """
        scored_alerts = []

        for detection, context, action in alerts:
            priority = self.calculate_priority(detection, context, action)
            scored_alerts.append((detection, context, action, priority))

        # Sort by overall_score descending
        scored_alerts.sort(key=lambda x: x[3].overall_score, reverse=True)

        return scored_alerts

    def _score_threat_level(self, threat_level: str) -> float:
        """Convert threat level to numeric score (0-100)."""
        return self.THREAT_SCORES.get(threat_level.lower(), 25)

    def _score_urgency(self, urgency: str) -> float:
        """Convert action urgency to numeric score (0-100)."""
        return self.URGENCY_SCORES.get(urgency.lower(), 25)

    def _score_confidence(self, confidence: float) -> float:
        """Convert detection confidence to score (0-100)."""
        # Confidence is already 0-1, scale to 0-100
        return confidence * 100

    def _score_size(self, size: str) -> float:
        """Convert size category to numeric score (0-100)."""
        return self.SIZE_SCORES.get(size.lower(), 30)

    def _determine_priority_level(self, score: float) -> str:
        """
        Map numeric score to priority level category.

        Args:
            score: Overall priority score (0-100)

        Returns:
            Priority level: critical, high, medium, or low
        """
        if score >= 80:
            return "critical"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "medium"
        else:
            return "low"

    def get_top_priorities(
        self,
        alerts: List[Tuple[Detection, EnrichedContext, ActionRecommendation]],
        top_n: int = 5
    ) -> List[Tuple[Detection, EnrichedContext, ActionRecommendation, PriorityScore]]:
        """
        Get the top N highest priority alerts.

        Args:
            alerts: List of alert tuples
            top_n: Number of top alerts to return (default: 5)

        Returns:
            List of top N alerts with priority scores
        """
        ranked = self.rank_alerts(alerts)
        return ranked[:top_n]


# Singleton instance
priority_agent = PriorityScoringAgent()
