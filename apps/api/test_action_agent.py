"""
Test Action Recommendation Agent
"""

import asyncio
from app.agents.action_agent import action_agent
from app.models.schemas import Detection, EnrichedContext, DetectionBox


async def test_action_agent():
    """Test the Action Recommendation Agent with various scenarios."""

    # Test Case 1: Critical bird in center screen
    print("\n" + "="*60)
    print("TEST 1: Critical Bird - Center Screen")
    print("="*60)

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

    action1 = await action_agent.recommend_action(detection1, context1)
    print(f"Primary Action: {action1.primary_action}")
    print(f"Secondary Action: {action1.secondary_action}")
    print(f"Reasoning: {action1.reasoning}")
    print(f"Urgency: {action1.urgency}")

    # Test Case 2: High threat drone - upper right
    print("\n" + "="*60)
    print("TEST 2: High Threat Drone - Upper Right")
    print("="*60)

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

    action2 = await action_agent.recommend_action(detection2, context2)
    print(f"Primary Action: {action2.primary_action}")
    print(f"Secondary Action: {action2.secondary_action}")
    print(f"Reasoning: {action2.reasoning}")
    print(f"Urgency: {action2.urgency}")

    # Test Case 3: Moderate balloon - lower left
    print("\n" + "="*60)
    print("TEST 3: Moderate Balloon - Lower Left")
    print("="*60)

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

    action3 = await action_agent.recommend_action(detection3, context3)
    print(f"Primary Action: {action3.primary_action}")
    print(f"Secondary Action: {action3.secondary_action}")
    print(f"Reasoning: {action3.reasoning}")
    print(f"Urgency: {action3.urgency}")

    # Test Case 4: Low threat kite - upper left
    print("\n" + "="*60)
    print("TEST 4: Low Threat Kite - Upper Left")
    print("="*60)

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

    action4 = await action_agent.recommend_action(detection4, context4)
    print(f"Primary Action: {action4.primary_action}")
    print(f"Secondary Action: {action4.secondary_action}")
    print(f"Reasoning: {action4.reasoning}")
    print(f"Urgency: {action4.urgency}")

    print("\n" + "="*60)
    print("All Action Agent Tests Complete!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_action_agent())
