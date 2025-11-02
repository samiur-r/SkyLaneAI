"""
Test Complete Alert Generation Workflow
Tests all 4 agents working together
"""

import asyncio
from app.workflows.alert_workflow import alert_workflow
from app.models.schemas import Detection, DetectionBox


async def test_single_alert():
    """Test generating a complete alert for a single detection."""
    print("\n" + "="*80)
    print("TEST 1: SINGLE COMPLETE ALERT")
    print("="*80)

    detection = Detection(
        class_name="bird",
        class_id=0,
        confidence=0.92,
        bbox=DetectionBox(x1=400, y1=300, x2=600, y2=500)
    )

    # Generate complete alert using all 4 agents
    alert = await alert_workflow.generate_complete_alert(
        detection,
        image_width=1920,
        image_height=1080
    )

    print(f"\n{alert.message.emoji} {alert.message.title}")
    print("-" * 80)
    print(f"\nDetection: {alert.detection.class_name.upper()}")
    print(f"Confidence: {alert.detection.confidence:.1%}")
    print(f"\nCONTEXT:")
    print(f"  Size: {alert.context.estimated_size}")
    print(f"  Position: {alert.context.screen_position}")
    print(f"  Threat Level: {alert.context.threat_level_raw}")
    print(f"  Area: {alert.context.bbox_area_pixels} pixels")
    print(f"\nMESSAGE:")
    print(f"{alert.message.body}")
    print(f"\nACTION RECOMMENDATION:")
    print(f"  Primary: {alert.action.primary_action}")
    print(f"  Secondary: {alert.action.secondary_action}")
    print(f"  Urgency: {alert.action.urgency}")
    print(f"  Reasoning: {alert.action.reasoning}")
    print(f"\nPRIORITY SCORE:")
    print(f"  Overall: {alert.priority.overall_score:.2f}")
    print(f"  Level: {alert.priority.priority_level.upper()}")
    print(f"  Factors:")
    for factor_name, factor_data in alert.priority.factors.items():
        print(f"    - {factor_name}: {factor_data['value']} "
              f"(score: {factor_data['score']}, weight: {factor_data['weight']})")


async def test_batch_alerts():
    """Test generating alerts for multiple detections."""
    print("\n" + "="*80)
    print("TEST 2: BATCH ALERT GENERATION")
    print("="*80)

    # Create multiple test detections
    detections = [
        Detection(
            class_name="bird",
        class_id=0,
            confidence=0.92,
            bbox=DetectionBox(x1=400, y1=300, x2=600, y2=500)
        ),
        Detection(
            class_name="drone",
        class_id=1,
            confidence=0.88,
            bbox=DetectionBox(x1=700, y1=100, x2=850, y2=250)
        ),
        Detection(
            class_name="balloon",
        class_id=2,
            confidence=0.78,
            bbox=DetectionBox(x1=100, y1=600, x2=200, y2=700)
        ),
        Detection(
            class_name="kite",
        class_id=3,
            confidence=0.65,
            bbox=DetectionBox(x1=50, y1=50, x2=120, y2=120)
        ),
        Detection(
            class_name="bird",
        class_id=0,
            confidence=0.95,
            bbox=DetectionBox(x1=450, y1=350, x2=650, y2=550)
        ),
    ]

    print(f"\nProcessing {len(detections)} detections...")

    # Generate alerts for all detections
    alerts = await alert_workflow.generate_batch_alerts(
        detections,
        image_width=1920,
        image_height=1080,
        return_top_n=3  # Only return top 3
    )

    print(f"\nTop {len(alerts)} Alerts (by priority):")
    print("-" * 80)

    for i, alert in enumerate(alerts, 1):
        print(f"\n#{i} - {alert.message.emoji} {alert.message.title}")
        print(f"   Priority: {alert.priority.overall_score:.2f} ({alert.priority.priority_level.upper()})")
        print(f"   Hazard: {alert.detection.class_name} ({alert.detection.confidence:.1%})")
        print(f"   Threat: {alert.context.threat_level_raw}")
        print(f"   Urgency: {alert.action.urgency}")
        print(f"   Action: {alert.action.primary_action}")


async def test_summary_report():
    """Test generating a summary report."""
    print("\n" + "="*80)
    print("TEST 3: SUMMARY REPORT")
    print("="*80)

    # Create a larger batch of detections
    detections = [
        Detection(
            class_name="bird",
        class_id=0,
            confidence=0.92,
            bbox=DetectionBox(x1=400, y1=300, x2=600, y2=500)
        ),
        Detection(
            class_name="drone",
        class_id=1,
            confidence=0.88,
            bbox=DetectionBox(x1=700, y1=100, x2=850, y2=250)
        ),
        Detection(
            class_name="balloon",
        class_id=2,
            confidence=0.78,
            bbox=DetectionBox(x1=100, y1=600, x2=200, y2=700)
        ),
        Detection(
            class_name="kite",
        class_id=3,
            confidence=0.65,
            bbox=DetectionBox(x1=50, y1=50, x2=120, y2=120)
        ),
        Detection(
            class_name="bird",
        class_id=0,
            confidence=0.95,
            bbox=DetectionBox(x1=450, y1=350, x2=650, y2=550)
        ),
        Detection(
            class_name="bird",
        class_id=0,
            confidence=0.70,
            bbox=DetectionBox(x1=200, y1=200, x2=280, y2=280)
        ),
        Detection(
            class_name="drone",
        class_id=1,
            confidence=0.82,
            bbox=DetectionBox(x1=500, y1=400, x2=650, y2=550)
        ),
    ]

    print(f"\nAnalyzing {len(detections)} detections...")

    # Generate summary report
    summary = await alert_workflow.generate_summary_report(
        detections,
        image_width=1920,
        image_height=1080
    )

    print(f"\nSUMMARY REPORT")
    print("-" * 80)
    print(f"\nTotal Detections: {summary['total_detections']}")
    print(f"Total Alerts Generated: {summary['total_alerts_generated']}")
    print(f"\nHazard Types:")
    for hazard, count in summary['hazard_types'].items():
        print(f"  - {hazard}: {count}")
    print(f"\nThreat Distribution:")
    for threat, count in summary['threat_distribution'].items():
        print(f"  - {threat}: {count}")
    print(f"\nPriority Distribution:")
    for priority, count in summary['priority_distribution'].items():
        print(f"  - {priority}: {count}")
    print(f"\nCritical Alerts: {summary['critical_count']}")
    print(f"High Priority Alerts: {summary['high_count']}")
    print(f"Require Immediate Attention: {summary['requires_immediate_attention']}")

    print(f"\nTop 5 Alerts:")
    for alert in summary['top_alerts'][:5]:
        print(f"\n  #{alert['rank']} - {alert['hazard'].upper()}")
        print(f"     Priority: {alert['priority_score']:.2f} ({alert['priority_level'].upper()})")
        print(f"     Threat: {alert['threat_level']}")
        print(f"     Message: {alert['message_title']}")
        print(f"     Action: {alert['primary_action']}")


async def main():
    """Run all workflow tests."""
    print("\n" + "="*80)
    print("COMPLETE ALERT GENERATION WORKFLOW TESTS")
    print("Testing all 4 agents: Context → Message → Action → Priority")
    print("="*80)

    # Test 1: Single alert
    await test_single_alert()

    # Test 2: Batch alerts
    await test_batch_alerts()

    # Test 3: Summary report
    await test_summary_report()

    print("\n" + "="*80)
    print("ALL WORKFLOW TESTS COMPLETE!")
    print("="*80)
    print("\nThe complete Natural Language Alert Generation system is working!")
    print("All 4 agents are integrated and operational:")
    print("  ✓ Context Enrichment Agent (rule-based)")
    print("  ✓ Message Crafting Agent (LLM-powered)")
    print("  ✓ Action Recommendation Agent (LLM-powered)")
    print("  ✓ Priority Scoring Agent (rule-based)")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
