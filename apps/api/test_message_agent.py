"""Test script for Message Crafting Agent"""

import sys
import asyncio
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.schemas import Detection, DetectionBox, EnrichedContext
from app.agents.message_agent import message_agent
from app.core.config import settings


async def test_message_crafting():
    """Test the message crafting agent with sample data"""

    print("=" * 70)
    print("Message Crafting Agent - Test Suite")
    print("=" * 70)

    # Check if API key is set
    if not settings.OPENAI_API_KEY:
        print("\n❌ OPENAI_API_KEY not set in environment")
        print("Please set OPENAI_API_KEY in your .env file to test this agent.")
        print("\nExample:")
        print("OPENAI_API_KEY=your_key_here")
        return 1

    print(f"\n✓ Using model: {settings.OPENAI_MODEL}")
    print(f"✓ Timeout: {settings.ALERT_GENERATION_TIMEOUT}s")

    # Test case
    detection = Detection(
        class_name="bird",
        class_id=14,
        confidence=0.87,
        bbox=DetectionBox(x1=1200, y1=200, x2=1400, y2=450),
        frame_number=1234,
        timestamp=41.13
    )

    context = EnrichedContext(
        estimated_size="large",
        bbox_area_pixels=50000,
        screen_position="upper-right",
        threat_level_raw="moderate"
    )

    print("\n" + "-" * 70)
    print("Test Case: Large Bird Detection")
    print("-" * 70)
    print(f"Input Detection:")
    print(f"  Class: {detection.class_name}")
    print(f"  Confidence: {detection.confidence:.1%}")
    print(f"  Position: {context.screen_position}")
    print(f"  Size: {context.estimated_size}")
    print(f"  Threat: {context.threat_level_raw}")

    try:
        print("\n🤖 Calling GPT-5-nano to craft message...")

        # Craft the message
        message = await message_agent.craft_message(detection, context)

        print("\n" + "=" * 70)
        print("Generated Alert Message")
        print("=" * 70)
        print(f"\n{message.emoji} {message.title}")
        print("\n" + message.body)
        print("\n" + "-" * 70)
        print("Parsed Sections:")
        for section_name, section_content in message.sections.items():
            print(f"\n[{section_name}]")
            print(section_content[:100] + "..." if len(section_content) > 100 else section_content)

        print("\n" + "=" * 70)
        print("✅ Message Crafting Test PASSED")
        print("=" * 70)
        print("\nMessage Statistics:")
        print(f"  Title Length: {len(message.title)} chars")
        print(f"  Body Length: {len(message.body)} chars")
        print(f"  Sections: {len(message.sections)}")
        print(f"  Emoji: {message.emoji}")

        return 0

    except Exception as e:
        print(f"\n❌ Message Crafting Test FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Run the test"""
    exit_code = asyncio.run(test_message_crafting())

    if exit_code == 0:
        print("\n🎉 All tests passed!")
        print("\nNext steps:")
        print("1. Integrate Message Agent into the video processing pipeline")
        print("2. Update UI to display crafted messages")
        print("3. Test with real video upload")
    else:
        print("\n⚠️  Tests failed. Please review the errors above.")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
