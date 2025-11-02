"""
Generate synthetic test video for SkyLaneAI hazard detection system.
Creates an aerial city scene with birds, drones, and balloons.
"""

import cv2
import numpy as np
from pathlib import Path

# Video configuration
WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 7  # seconds
TOTAL_FRAMES = FPS * DURATION

# Output path
OUTPUT_PATH = Path(__file__).parent / "temp" / "uploads" / "test_aerial_hazards.mp4"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def create_gradient_sky(width, height, frame_num, total_frames):
    """Create animated sunset sky gradient."""
    # Sunset colors (BGR format)
    progress = frame_num / total_frames

    # Top color (deep blue to orange)
    top_b = int(180 - 50 * progress)
    top_g = int(120 + 50 * progress)
    top_r = int(60 + 80 * progress)

    # Bottom color (orange to pink)
    bottom_b = int(100 + 30 * progress)
    bottom_g = int(140 + 40 * progress)
    bottom_r = int(255)

    # Create gradient
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        ratio = y / height
        b = int(top_b * (1 - ratio) + bottom_b * ratio)
        g = int(top_g * (1 - ratio) + bottom_g * ratio)
        r = int(top_r * (1 - ratio) + bottom_r * ratio)
        gradient[y, :] = [b, g, r]

    return gradient

def draw_buildings(frame, frame_num, total_frames):
    """Draw simplified city skyline with parallax effect."""
    height, width = frame.shape[:2]
    horizon = int(height * 0.7)

    # Camera movement (slow forward pan)
    offset = int((frame_num / total_frames) * 100)

    # Building parameters
    buildings = [
        # (x, width, height, brightness)
        (100 - offset, 150, 300, 60),
        (300 - offset, 200, 400, 70),
        (550 - offset, 120, 250, 55),
        (720 - offset, 180, 380, 75),
        (950 - offset, 160, 320, 65),
        (1150 - offset, 220, 420, 80),
        (1420 - offset, 140, 280, 60),
        (1600 - offset, 190, 360, 72),
        (1850 - offset, 170, 340, 68),
    ]

    for x, w, h, brightness in buildings:
        if x + w > 0 and x < width:  # Only draw visible buildings
            # Building body
            color = (brightness, brightness, brightness)
            cv2.rectangle(frame,
                         (x, horizon - h),
                         (x + w, horizon),
                         color, -1)

            # Windows with sunset reflection
            window_color = (80 + brightness, 120 + brightness, 200 + brightness)
            for wy in range(horizon - h + 20, horizon - 10, 30):
                for wx in range(x + 10, x + w - 10, 25):
                    cv2.rectangle(frame,
                                (wx, wy),
                                (wx + 15, wy + 20),
                                window_color, -1)

            # Building outline
            cv2.rectangle(frame,
                         (x, horizon - h),
                         (x + w, horizon),
                         (40, 40, 40), 2)

def draw_drone(frame, x, y, size=30):
    """Draw a simple quadcopter drone."""
    # Drone body (center)
    cv2.circle(frame, (int(x), int(y)), size // 3, (50, 50, 50), -1)

    # Four arms
    arm_length = size
    arm_positions = [
        (-arm_length, -arm_length),  # top-left
        (arm_length, -arm_length),   # top-right
        (-arm_length, arm_length),   # bottom-left
        (arm_length, arm_length)     # bottom-right
    ]

    for dx, dy in arm_positions:
        cv2.line(frame,
                (int(x), int(y)),
                (int(x + dx), int(y + dy)),
                (40, 40, 40), 3)
        # Propeller
        cv2.circle(frame, (int(x + dx), int(y + dy)), size // 4, (80, 80, 80), -1)
        cv2.circle(frame, (int(x + dx), int(y + dy)), size // 4, (120, 120, 120), 1)

def draw_bird(frame, x, y, wing_angle, size=20):
    """Draw a simple bird silhouette."""
    # Bird body
    body_points = np.array([
        [x, y],
        [x - size // 3, y + size // 2],
        [x + size // 3, y + size // 2]
    ], dtype=np.int32)
    cv2.fillPoly(frame, [body_points], (30, 30, 30))

    # Wings (animated)
    wing_offset = int(size * np.sin(wing_angle))
    # Left wing
    left_wing = np.array([
        [x - size // 3, y],
        [x - size * 1.5, y - wing_offset],
        [x - size // 2, y + size // 3]
    ], dtype=np.int32)
    cv2.fillPoly(frame, [left_wing], (20, 20, 20))

    # Right wing
    right_wing = np.array([
        [x + size // 3, y],
        [x + size * 1.5, y - wing_offset],
        [x + size // 2, y + size // 3]
    ], dtype=np.int32)
    cv2.fillPoly(frame, [right_wing], (20, 20, 20))

def draw_balloon(frame, x, y, color, size=40):
    """Draw a balloon."""
    # Balloon body
    cv2.ellipse(frame, (int(x), int(y)), (size, int(size * 1.2)), 0, 0, 360, color, -1)
    cv2.ellipse(frame, (int(x), int(y)), (size, int(size * 1.2)), 0, 0, 360, (0, 0, 0), 2)

    # Highlight
    highlight_offset = size // 3
    cv2.ellipse(frame,
               (int(x - highlight_offset), int(y - highlight_offset)),
               (size // 4, size // 3), 0, 0, 360,
               (min(255, color[0] + 80), min(255, color[1] + 80), min(255, color[2] + 80)), -1)

    # String
    string_points = []
    for i in range(10):
        sx = x + np.sin(i * 0.5) * 3
        sy = y + size * 1.2 + i * 8
        string_points.append([int(sx), int(sy)])
    string_points = np.array(string_points, dtype=np.int32)
    cv2.polylines(frame, [string_points], False, (100, 100, 100), 2)

def generate_video():
    """Generate the complete test video."""
    print(f"Generating test video: {OUTPUT_PATH}")
    print(f"Resolution: {WIDTH}x{HEIGHT}, FPS: {FPS}, Duration: {DURATION}s")

    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(OUTPUT_PATH), fourcc, FPS, (WIDTH, HEIGHT))

    # Object trajectories
    # Drone: flies from left to right
    drone_start_x = -100
    drone_end_x = WIDTH + 100
    drone_y = HEIGHT // 3

    # Birds: flock flying across
    num_birds = 5
    birds_start_x = WIDTH + 100
    birds_end_x = -100
    birds_base_y = HEIGHT // 4

    # Balloons: drifting upward
    balloons = [
        {"x": WIDTH * 0.3, "y": HEIGHT * 0.8, "color": (0, 0, 255), "speed": 1.5},    # Red
        {"x": WIDTH * 0.35, "y": HEIGHT * 0.85, "color": (255, 0, 0), "speed": 1.2},  # Blue
        {"x": WIDTH * 0.32, "y": HEIGHT * 0.75, "color": (0, 255, 255), "speed": 1.8} # Yellow
    ]

    for frame_num in range(TOTAL_FRAMES):
        # Create sky background
        frame = create_gradient_sky(WIDTH, HEIGHT, frame_num, TOTAL_FRAMES)

        # Draw buildings
        draw_buildings(frame, frame_num, TOTAL_FRAMES)

        # Animate drone
        progress = frame_num / TOTAL_FRAMES
        drone_x = drone_start_x + (drone_end_x - drone_start_x) * progress
        drone_y_wave = drone_y + np.sin(progress * 4 * np.pi) * 30  # Slight wave motion
        if -50 < drone_x < WIDTH + 50:  # Only draw when visible
            draw_drone(frame, drone_x, drone_y_wave, size=35)

        # Animate birds
        birds_x = birds_start_x + (birds_end_x - birds_start_x) * progress
        for i in range(num_birds):
            bird_x = birds_x + i * 60 + np.sin(progress * 6 * np.pi + i) * 20
            bird_y = birds_base_y + i * 30 + np.cos(progress * 5 * np.pi + i) * 15
            wing_angle = frame_num * 0.3 + i  # Wing flapping animation
            if -50 < bird_x < WIDTH + 50:
                draw_bird(frame, int(bird_x), int(bird_y), wing_angle, size=25)

        # Animate balloons
        for balloon in balloons:
            balloon["y"] -= balloon["speed"]  # Drift upward
            balloon["x"] += np.sin(frame_num * 0.05) * 0.5  # Slight horizontal drift
            if balloon["y"] > -100:  # Only draw if visible
                draw_balloon(frame, balloon["x"], balloon["y"], balloon["color"], size=45)

        # Add subtle clouds
        if frame_num % 10 == 0:  # Draw clouds every few frames for variety
            cloud_alpha = 0.3
            overlay = frame.copy()
            cv2.ellipse(overlay, (WIDTH // 4, HEIGHT // 5), (150, 60), 0, 0, 360, (255, 255, 255), -1)
            cv2.ellipse(overlay, (WIDTH * 3 // 4, HEIGHT // 6), (180, 70), 0, 0, 360, (255, 255, 255), -1)
            cv2.addWeighted(overlay, cloud_alpha, frame, 1 - cloud_alpha, 0, frame)

        # Write frame
        out.write(frame)

        # Progress indicator
        if (frame_num + 1) % 30 == 0:
            print(f"Progress: {frame_num + 1}/{TOTAL_FRAMES} frames ({(frame_num + 1) / TOTAL_FRAMES * 100:.1f}%)")

    out.release()
    print(f"✓ Video generated successfully: {OUTPUT_PATH}")
    print(f"File size: {OUTPUT_PATH.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    generate_video()
