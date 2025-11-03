"""Test script for YOLO-World detector"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from ultralytics import YOLOWorld
import numpy as np
import cv2

def test_yolo_world():
    """Test YOLO-World model loading and detection"""

    print("=" * 60)
    print("YOLO-World Test Script")
    print("=" * 60)

    # Test 1: Load model
    print("\n1. Loading YOLO-World model...")
    try:
        model = YOLOWorld("yolov8l-world.pt")
        print("✓ Model loaded successfully!")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

    # Test 2: Set custom classes
    print("\n2. Setting custom classes (zero-shot)...")
    try:
        classes = ["drone", "bird", "airplane", "helicopter", "balloon", "kite"]
        model.set_classes(classes)
        print(f"✓ Classes configured: {', '.join(classes)}")
    except Exception as e:
        print(f"✗ Error setting classes: {e}")
        return False

    # Test 3: Test detection on a blank image
    print("\n3. Testing detection on sample image...")
    try:
        # Create a dummy image (blue sky)
        test_image = np.ones((640, 640, 3), dtype=np.uint8) * 135  # Sky blue

        # Add some random shapes to simulate objects
        cv2.circle(test_image, (200, 200), 30, (100, 100, 100), -1)  # Dark circle
        cv2.rectangle(test_image, (400, 300), (450, 350), (80, 80, 80), -1)  # Dark rectangle

        results = model.predict(test_image, conf=0.15, verbose=False)
        print(f"✓ Detection completed! Found {len(results[0].boxes)} objects")

        if len(results[0].boxes) > 0:
            for i, box in enumerate(results[0].boxes):
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                cls_name = results[0].names[cls_id]
                print(f"  - Object {i+1}: {cls_name} ({conf:.2%} confidence)")
        else:
            print("  (No objects detected in test image - this is expected)")

    except Exception as e:
        print(f"✗ Error during detection: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 4: Check device
    print("\n4. Checking device configuration...")
    try:
        device = model.device
        print(f"✓ Model running on: {device}")
    except Exception as e:
        print(f"✗ Error checking device: {e}")

    print("\n" + "=" * 60)
    print("✓ All tests passed! YOLO-World is ready to use.")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Start the FastAPI server: uvicorn app.main:app --reload")
    print("  2. Upload videos at: http://localhost:8000/docs")
    print("  3. Detect drones, birds, balloons, and more!")
    print("\n")

    return True

if __name__ == "__main__":
    try:
        success = test_yolo_world()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
