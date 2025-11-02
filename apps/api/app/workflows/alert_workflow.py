"""
Complete Alert Generation Workflow
Orchestrates all 4 agents to generate natural language alerts.
"""

import asyncio
from typing import List, Tuple, Optional

from app.models.schemas import (
    Detection,
    EnrichedContext,
    CraftedMessage,
    ActionRecommendation,
    PriorityScore,
    NaturalLanguageAlert
)
from app.agents.context_agent import context_agent
from app.agents.message_agent import message_agent
from app.agents.action_agent import action_agent
from app.agents.priority_agent import priority_agent


class AlertGenerationWorkflow:
    """
    Orchestrates the 4-agent pipeline for natural language alert generation.

    Pipeline:
    1. Context Enrichment (rule-based, fast)
    2. Message Crafting (LLM-powered)
    3. Action Recommendation (LLM-powered)
    4. Priority Scoring (rule-based, fast)

    The workflow can process single detections or batches.
    """

    async def generate_complete_alert(
        self,
        detection: Detection,
        image_width: Optional[int] = None,
        image_height: Optional[int] = None
    ) -> NaturalLanguageAlert:
        """
        Generate a complete natural language alert for a single detection.

        Args:
            detection: The hazard detection
            image_width: Video/image width in pixels (optional)
            image_height: Video/image height in pixels (optional)

        Returns:
            Complete NaturalLanguageAlert with all components
        """
        # Step 1: Enrich context (rule-based, instant)
        context = context_agent.enrich(detection, image_width, image_height)

        # Steps 2 & 3: Run message and action in parallel (both use LLM)
        message_task = message_agent.craft_message(detection, context)
        action_task = action_agent.recommend_action(detection, context)

        message, action = await asyncio.gather(message_task, action_task)

        # Step 4: Calculate priority (rule-based, instant)
        priority = priority_agent.calculate_priority(detection, context, action)

        # Assemble complete alert
        alert = NaturalLanguageAlert(
            detection=detection,
            context=context,
            message=message,
            action=action,
            priority=priority
        )

        return alert

    async def generate_batch_alerts(
        self,
        detections: List[Detection],
        image_width: Optional[int] = None,
        image_height: Optional[int] = None,
        return_top_n: Optional[int] = None
    ) -> List[NaturalLanguageAlert]:
        """
        Generate alerts for multiple detections in batch.

        Args:
            detections: List of hazard detections
            image_width: Video/image width (optional)
            image_height: Video/image height (optional)
            return_top_n: If specified, only return top N by priority (optional)

        Returns:
            List of NaturalLanguageAlerts, sorted by priority (highest first)
        """
        if not detections:
            return []

        # Step 1: Enrich all contexts (batch, fast)
        contexts = await asyncio.to_thread(
            context_agent.enrich_batch,
            detections,
            image_width,
            image_height
        )

        # Steps 2 & 3: Generate messages and actions in parallel
        message_tasks = [
            message_agent.craft_message(det, ctx)
            for det, ctx in zip(detections, contexts)
        ]
        action_tasks = [
            action_agent.recommend_action(det, ctx)
            for det, ctx in zip(detections, contexts)
        ]

        all_tasks = message_tasks + action_tasks
        results = await asyncio.gather(*all_tasks)

        # Split results
        messages = results[:len(detections)]
        actions = results[len(detections):]

        # Step 4: Calculate priorities for all
        priorities = [
            priority_agent.calculate_priority(det, ctx, act)
            for det, ctx, act in zip(detections, contexts, actions)
        ]

        # Assemble complete alerts
        alerts = [
            NaturalLanguageAlert(
                detection=det,
                context=ctx,
                message=msg,
                action=act,
                priority=pri
            )
            for det, ctx, msg, act, pri in zip(
                detections, contexts, messages, actions, priorities
            )
        ]

        # Sort by priority score (highest first)
        alerts.sort(key=lambda a: a.priority.overall_score, reverse=True)

        # Return top N if specified
        if return_top_n is not None:
            alerts = alerts[:return_top_n]

        return alerts

    async def generate_summary_report(
        self,
        detections: List[Detection],
        image_width: Optional[int] = None,
        image_height: Optional[int] = None
    ) -> dict:
        """
        Generate a summary report of all detections with analytics.

        Args:
            detections: List of all detections from video
            image_width: Video width
            image_height: Video height

        Returns:
            Summary report with statistics and top alerts
        """
        if not detections:
            return {
                "total_detections": 0,
                "top_alerts": [],
                "threat_distribution": {},
                "hazard_types": {}
            }

        # Generate alerts for all detections
        alerts = await self.generate_batch_alerts(
            detections,
            image_width,
            image_height
        )

        # Calculate statistics
        threat_distribution = {}
        hazard_types = {}
        priority_distribution = {}

        for alert in alerts:
            # Threat level distribution
            threat = alert.context.threat_level_raw
            threat_distribution[threat] = threat_distribution.get(threat, 0) + 1

            # Hazard type distribution
            hazard = alert.detection.class_name
            hazard_types[hazard] = hazard_types.get(hazard, 0) + 1

            # Priority level distribution
            priority_level = alert.priority.priority_level
            priority_distribution[priority_level] = \
                priority_distribution.get(priority_level, 0) + 1

        # Get top 10 highest priority alerts
        top_alerts = alerts[:10]

        return {
            "total_detections": len(detections),
            "total_alerts_generated": len(alerts),
            "threat_distribution": threat_distribution,
            "hazard_types": hazard_types,
            "priority_distribution": priority_distribution,
            "top_alerts": [
                {
                    "rank": i + 1,
                    "hazard": alert.detection.class_name,
                    "priority_score": alert.priority.overall_score,
                    "priority_level": alert.priority.priority_level,
                    "threat_level": alert.context.threat_level_raw,
                    "message_title": alert.message.title,
                    "primary_action": alert.action.primary_action,
                    "urgency": alert.action.urgency
                }
                for i, alert in enumerate(top_alerts)
            ],
            "critical_count": priority_distribution.get("critical", 0),
            "high_count": priority_distribution.get("high", 0),
            "requires_immediate_attention": sum(
                1 for a in alerts if a.action.urgency == "immediate"
            )
        }


# Singleton instance
alert_workflow = AlertGenerationWorkflow()
