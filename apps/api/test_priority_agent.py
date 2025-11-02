"""
Test Priority Scoring Agent
"""

from app.agents.priority_agent import priority_agent
from app.models.schemas import Detection, EnrichedContext, ActionRecommendation, DetectionBox


def test_priority_scoring():
    """Test the Priority Scoring Agent with various scenarios."""

    print("\n" + "="*60)
    print("PRIORITY SCORING AGENT TESTS")
    print("="*60)

    # Create test alerts with varying severity
    alerts = []

    # Alert 1: Critical bird in center
    detection1 = Detection(
        class_name="bird",
        class_id=0,
        confidence=0.92,
        bbox=DetectionBox(x1=400, y1=300, x2=600, y2=500)
    )
    context1 = EnrichedContext(
        estimated_size="large",
        bbox_area_pixels=40000,
        screen_position="center",
        threat_level_raw="critical"
    )
    action1 = ActionRecommendation(
        primary_action="Execute immediate evasive maneuver",
        secondary_action="Alert air traffic control",
        reasoning="Critical threat requires immediate action",
        urgency="immediate"
    )
    alerts.append((detection1, context1, action1))

    # Alert 2: High threat drone
    detection2 = Detection(
        class_name="drone",
        class_id=1,
        confidence=0.85,
        bbox=DetectionBox(x1=700, y1=100, x2=850, y2=250)
    )
    context2 = EnrichedContext(
        estimated_size="medium",
        bbox_area_pixels=22500,
        screen_position="upper-right",
        threat_level_raw="high"
    )
    action2 = ActionRecommendation(
        primary_action="Reduce speed and monitor closely",
        secondary_action="Prepare evasive action",
        reasoning="High threat requires cautious monitoring",
        urgency="urgent"
    )
    alerts.append((detection2, context2, action2))

    # Alert 3: Moderate balloon
    detection3 = Detection(
        class_name="balloon",
        class_id=2,
        confidence=0.78,
        bbox=DetectionBox(x1=100, y1=600, x2=200, y2=700)
    )
    context3 = EnrichedContext(
        estimated_size="small",
        bbox_area_pixels=10000,
        screen_position="lower-left",
        threat_level_raw="moderate"
    )
    action3 = ActionRecommendation(
        primary_action="Maintain awareness of position",
        secondary_action="Adjust course if needed",
        reasoning="Moderate threat requires monitoring",
        urgency="caution"
    )
    alerts.append((detection3, context3, action3))

    # Alert 4: Low threat kite
    detection4 = Detection(
        class_name="kite",
        class_id=3,
        confidence=0.65,
        bbox=DetectionBox(x1=50, y1=50, x2=120, y2=120)
    )
    context4 = EnrichedContext(
        estimated_size="small",
        bbox_area_pixels=4900,
        screen_position="upper-left",
        threat_level_raw="low"
    )
    action4 = ActionRecommendation(
        primary_action="Continue current flight path",
        secondary_action="Maintain standard vigilance",
        reasoning="Low threat, distant hazard",
        urgency="advisory"
    )
    alerts.append((detection4, context4, action4))

    # Alert 5: High confidence critical
    detection5 = Detection(
        class_name="bird",
        class_id=0,
        confidence=0.96,
        bbox=DetectionBox(x1=450, y1=350, x2=650, y2=550)
    )
    context5 = EnrichedContext(
        estimated_size="large",
        bbox_area_pixels=40000,
        screen_position="center",
        threat_level_raw="critical"
    )
    action5 = ActionRecommendation(
        primary_action="Immediate ascent maneuver",
        secondary_action="Alert all systems",
        reasoning="Critical collision risk",
        urgency="immediate"
    )
    alerts.append((detection5, context5, action5))

    # Test individual scoring
    print("\n" + "="*60)
    print("INDIVIDUAL ALERT SCORES")
    print("="*60)

    for i, (detection, context, action) in enumerate(alerts, 1):
        priority = priority_agent.calculate_priority(detection, context, action)
        print(f"\nAlert {i}: {detection.class_name.upper()}")
        print(f"Overall Score: {priority.overall_score:.2f}")
        print(f"Priority Level: {priority.priority_level.upper()}")
        print(f"Factors:")
        for factor_name, factor_data in priority.factors.items():
            print(f"  - {factor_name}: {factor_data['value']} "
                  f"(score: {factor_data['score']}, weight: {factor_data['weight']})")

    # Test ranking
    print("\n" + "="*60)
    print("RANKED ALERTS (Highest Priority First)")
    print("="*60)

    ranked_alerts = priority_agent.rank_alerts(alerts)

    for rank, (detection, context, action, priority) in enumerate(ranked_alerts, 1):
        print(f"\n#{rank} - {detection.class_name.upper()} "
              f"(Score: {priority.overall_score:.2f}, "
              f"Level: {priority.priority_level.upper()})")
        print(f"   Confidence: {detection.confidence:.1%}, "
              f"Threat: {context.threat_level_raw}, "
              f"Urgency: {action.urgency}")

    # Test top priorities
    print("\n" + "="*60)
    print("TOP 3 PRIORITIES")
    print("="*60)

    top_3 = priority_agent.get_top_priorities(alerts, top_n=3)

    for rank, (detection, context, action, priority) in enumerate(top_3, 1):
        print(f"\n#{rank} - {detection.class_name.upper()}")
        print(f"   Score: {priority.overall_score:.2f}")
        print(f"   Level: {priority.priority_level.upper()}")
        print(f"   Action: {action.primary_action}")

    print("\n" + "="*60)
    print("All Priority Scoring Tests Complete!")
    print("="*60)


if __name__ == "__main__":
    test_priority_scoring()
