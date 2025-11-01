"""Test script for Context Enrichment Agent"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.schemas import Detection, DetectionBox
from app.agents.context_agent import context_agent


def test_context_enrichment():
    """Test the context enrichment agent with sample detections"""

    print("=" * 70)
    print("Context Enrichment Agent - Test Suite")
    print("=" * 70)

    # Test cases with different scenarios
    test_cases = [
        {
            "name": "Large bird, upper-right, high confidence",
            "detection": Detection(
                class_name="bird",
                class_id=14,
                confidence=0.87,
                bbox=DetectionBox(x1=1200, y1=200, x2=1400, y2=450),  # Large area
                frame_number=1234,
                timestamp=41.13
            ),
            "image_width": 1920,
            "image_height": 1080
        },
        {
            "name": "Small drone, center, medium confidence",
            "detection": Detection(
                class_name="airplane",  # Might be detected as airplane
                class_id=4,
                confidence=0.65,
                bbox=DetectionBox(x1=900, y1=500, x2=1020, y2=580),  # Small area
                frame_number=567,
                timestamp=18.9
            ),
            "image_width": 1920,
            "image_height": 1080
        },
        {
            "name": "Medium balloon, lower-left, very high confidence",
            "detection": Detection(
                class_name="sports ball",  # Might be a balloon
                class_id=32,
                confidence=0.92,
                bbox=DetectionBox(x1=200, y1=800, x2=450, y2=1000),  # Medium area
                frame_number=890,
                timestamp=29.67
            ),
            "image_width": 1920,
            "image_height": 1080
        },
        {
            "name": "Large kite, upper-left, low confidence",
            "detection": Detection(
                class_name="kite",
                class_id=33,
                confidence=0.48,
                bbox=DetectionBox(x1=100, y1=50, x2=500, y2=400),  # Large area
                frame_number=1500,
                timestamp=50.0
            ),
            "image_width": 1920,
            "image_height": 1080
        }
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("-" * 70)

        detection = test_case["detection"]

        # Display detection info
        print(f"Input Detection:")
        print(f"  Class: {detection.class_name}")
        print(f"  Confidence: {detection.confidence:.1%}")
        print(f"  BBox: ({detection.bbox.x1:.0f}, {detection.bbox.y1:.0f}) to "
              f"({detection.bbox.x2:.0f}, {detection.bbox.y2:.0f})")
        print(f"  Frame: {detection.frame_number} @ {detection.timestamp:.2f}s")

        try:
            # Enrich the detection
            context = context_agent.enrich(
                detection,
                test_case["image_width"],
                test_case["image_height"]
            )

            # Display enriched context
            print(f"\nEnriched Context:")
            print(f"  ✓ Size Category: {context.estimated_size}")
            print(f"  ✓ BBox Area: {context.bbox_area_pixels:,} pixels²")
            print(f"  ✓ Screen Position: {context.screen_position}")
            print(f"  ✓ Threat Level: {context.threat_level_raw}")

            # Calculate screen coverage
            total_area = test_case["image_width"] * test_case["image_height"]
            coverage_pct = (context.bbox_area_pixels / total_area) * 100
            print(f"  ✓ Screen Coverage: {coverage_pct:.2f}%")

            # Validate results
            assert context.estimated_size in ["small", "medium", "large"], \
                f"Invalid size: {context.estimated_size}"
            assert context.bbox_area_pixels > 0, "BBox area must be positive"
            assert context.screen_position, "Position should not be empty"
            assert context.threat_level_raw in ["low", "moderate", "high", "critical"], \
                f"Invalid threat level: {context.threat_level_raw}"

            print(f"  ✅ Test PASSED")

        except Exception as e:
            print(f"  ❌ Test FAILED: {e}")
            all_passed = False

    # Test batch enrichment
    print(f"\n\nBatch Enrichment Test")
    print("-" * 70)

    try:
        detections = [tc["detection"] for tc in test_cases]
        contexts = context_agent.enrich_batch(detections, 1920, 1080)

        print(f"Input: {len(detections)} detections")
        print(f"Output: {len(contexts)} enriched contexts")

        assert len(contexts) == len(detections), "Batch size mismatch"

        print("✅ Batch enrichment PASSED")

    except Exception as e:
        print(f"❌ Batch enrichment FAILED: {e}")
        all_passed = False

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nThe Context Enrichment Agent is working correctly.")
        print("\nNext steps:")
        print("1. Start the FastAPI server: uvicorn app.main:app --reload")
        print("2. Upload a video through the UI")
        print("3. Check the WebSocket detection messages for 'context' field")
        print("\nEach detection should now include:")
        print("  - estimated_size (small/medium/large)")
        print("  - bbox_area_pixels")
        print("  - screen_position")
        print("  - threat_level_raw (low/moderate/high/critical)")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = test_context_enrichment()
    sys.exit(exit_code)
