"""
Script to add synthetic test objects (drone, balloons, birds) to a video
for testing the SkyLaneAI detection system.
"""

import cv2
import numpy as np
import sys
from pathlib import Path

def draw_drone(frame, x, y, size=60):
    """Draw a simple drone shape"""
    # Drone body (rectangle)
    cv2.rectangle(frame, (x-size//2, y-10), (x+size//2, y+10), (80, 80, 80), -1)

    # Propellers (circles)
    prop_offset = size//2 - 5
    cv2.circle(frame, (x-prop_offset, y-15), 8, (200, 200, 200), -1)
    cv2.circle(frame, (x+prop_offset, y-15), 8, (200, 200, 200), -1)
    cv2.circle(frame, (x-prop_offset, y+15), 8, (200, 200, 200), -1)
    cv2.circle(frame, (x+prop_offset, y+15), 8, (200, 200, 200), -1)

    # Camera (small rectangle)
    cv2.rectangle(frame, (x-5, y+12), (x+5, y+18), (40, 40, 40), -1)

def draw_balloon(frame, x, y, color, size=40):
    """Draw a balloon shape"""
    # Balloon (circle)
    cv2.circle(frame, (x, y), size//2, color, -1)
    # Highlight
    cv2.circle(frame, (x-size//6, y-size//6), size//8, (255, 255, 255), -1)
    # String
    pts = np.array([[x, y+size//2], [x-5, y+size], [x+3, y+size+20]], np.int32)
    cv2.polylines(frame, [pts], False, (100, 100, 100), 2)

def draw_bird(frame, x, y, wing_angle=0, size=30):
    """Draw a simple bird shape with animated wings"""
    # Bird body (ellipse)
    cv2.ellipse(frame, (x, y), (size//3, size//4), 0, 0, 360, (60, 60, 60), -1)

    # Wings (two curved lines)
    wing_spread = int(size * abs(np.sin(wing_angle)))
    left_wing = np.array([
        [x, y],
        [x-wing_spread, y-size//3],
        [x-wing_spread-10, y]
    ], np.int32)
    right_wing = np.array([
        [x, y],
        [x+wing_spread, y-size//3],
        [x+wing_spread+10, y]
    ], np.int32)

    cv2.polylines(frame, [left_wing], False, (40, 40, 40), 2)
    cv2.polylines(frame, [right_wing], False, (40, 40, 40), 2)

    # Beak (small triangle)
    beak = np.array([[x+size//3, y], [x+size//2, y-3], [x+size//2, y+3]], np.int32)
    cv2.fillPoly(frame, [beak], (200, 150, 50))

def add_objects_to_video(input_path, output_path):
    """Add test objects to video at different timeframes"""

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_path}")
        return False

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Video info: {width}x{height}, {fps} FPS, {total_frames} frames")

    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0

    # Object trajectories (start_frame, end_frame, start_pos, end_pos, object_type)
    objects = [
        # Drone - appears early, moves left to right
        {
            'type': 'drone',
            'start_frame': int(total_frames * 0.15),
            'end_frame': int(total_frames * 0.35),
            'start_x': width * 0.2,
            'end_x': width * 0.8,
            'y': height * 0.3,
        },
        # Balloon 1 (red) - middle section, moving slowly upward
        {
            'type': 'balloon',
            'color': (50, 50, 255),  # Red in BGR
            'start_frame': int(total_frames * 0.4),
            'end_frame': int(total_frames * 0.7),
            'start_x': width * 0.3,
            'end_x': width * 0.35,
            'start_y': height * 0.6,
            'end_y': height * 0.3,
        },
        # Balloon 2 (blue) - middle section, moving slowly upward
        {
            'type': 'balloon',
            'color': (255, 100, 50),  # Blue in BGR
            'start_frame': int(total_frames * 0.45),
            'end_frame': int(total_frames * 0.75),
            'start_x': width * 0.6,
            'end_x': width * 0.65,
            'start_y': height * 0.7,
            'end_y': height * 0.4,
        },
        # Bird 1 - early section, flying diagonally
        {
            'type': 'bird',
            'start_frame': int(total_frames * 0.1),
            'end_frame': int(total_frames * 0.25),
            'start_x': width * 0.1,
            'end_x': width * 0.4,
            'start_y': height * 0.2,
            'end_y': height * 0.35,
        },
        # Bird 2 - middle section, flying right to left
        {
            'type': 'bird',
            'start_frame': int(total_frames * 0.5),
            'end_frame': int(total_frames * 0.65),
            'start_x': width * 0.9,
            'end_x': width * 0.3,
            'start_y': height * 0.25,
            'end_y': height * 0.3,
        },
        # Bird 3 - late section, flying across
        {
            'type': 'bird',
            'start_frame': int(total_frames * 0.75),
            'end_frame': int(total_frames * 0.95),
            'start_x': width * 0.2,
            'end_x': width * 0.7,
            'start_y': height * 0.4,
            'end_y': height * 0.35,
        },
    ]

    print("Processing frames...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Draw each object if it's active in this frame
        for obj in objects:
            if obj['start_frame'] <= frame_count <= obj['end_frame']:
                # Calculate position based on interpolation
                progress = (frame_count - obj['start_frame']) / (obj['end_frame'] - obj['start_frame'])

                x = int(obj['start_x'] + (obj['end_x'] - obj['start_x']) * progress)

                if obj['type'] == 'drone':
                    y = int(obj['y'])
                    draw_drone(frame, x, y)

                elif obj['type'] == 'balloon':
                    y = int(obj['start_y'] + (obj['end_y'] - obj['start_y']) * progress)
                    draw_balloon(frame, x, y, obj['color'])

                elif obj['type'] == 'bird':
                    y = int(obj['start_y'] + (obj['end_y'] - obj['start_y']) * progress)
                    # Animate wing flapping
                    wing_angle = frame_count * 0.3
                    draw_bird(frame, x, y, wing_angle)

        out.write(frame)
        frame_count += 1

        if frame_count % 30 == 0:
            print(f"Processed {frame_count}/{total_frames} frames ({frame_count*100//total_frames}%)")

    cap.release()
    out.release()

    print(f"\n✓ Successfully created test video: {output_path}")
    print(f"Objects added:")
    print(f"  - 1 Drone (frames {objects[0]['start_frame']}-{objects[0]['end_frame']})")
    print(f"  - 2 Balloons (red and blue)")
    print(f"  - 3 Birds at different times")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_test_objects.py <input_video_path> [output_video_path]")
        print("\nExample:")
        print("  python add_test_objects.py ../temp/uploads/video.mp4")
        print("  python add_test_objects.py ../temp/uploads/video.mp4 ../temp/uploads/test_video.mp4")
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        # Create output filename
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_with_objects{input_file.suffix}")

    if not Path(input_path).exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    success = add_objects_to_video(input_path, output_path)
    sys.exit(0 if success else 1)
