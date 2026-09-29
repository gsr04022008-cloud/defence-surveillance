import cv2
import numpy as np
import random
import math
import time


WIDTH = 700
HEIGHT = 700
CENTER = (WIDTH // 2, HEIGHT // 2)
MAX_RADIUS = 300


targets = []


def create_target():
    angle = random.uniform(0, 360)
    distance = random.uniform(60, MAX_RADIUS)

    return {
        "angle": angle,
        "distance": distance,
        "speed": random.uniform(0.5, 2.0)
    }


# Create initial simulated targets
for _ in range(8):
    targets.append(create_target())


while True:

    # Create black radar screen
    radar = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Draw radar circles
    for radius in range(75, MAX_RADIUS + 1, 75):
        cv2.circle(
            radar,
            CENTER,
            radius,
            (0, 100, 0),
            1
        )

    # Draw cross lines
    cv2.line(
        radar,
        (CENTER[0] - MAX_RADIUS, CENTER[1]),
        (CENTER[0] + MAX_RADIUS, CENTER[1]),
        (0, 100, 0),
        1
    )

    cv2.line(
        radar,
        (CENTER[0], CENTER[1] - MAX_RADIUS),
        (CENTER[0], CENTER[1] + MAX_RADIUS),
        (0, 100, 0),
        1
    )

    # Draw center
    cv2.circle(
        radar,
        CENTER,
        5,
        (0, 255, 0),
        -1
    )

    # Update and draw targets
    for target in targets:

        target["distance"] += target["speed"]

        # Reset target when it reaches the edge
        if target["distance"] > MAX_RADIUS:
            target["distance"] = 30
            target["angle"] = random.uniform(0, 360)

        angle_rad = math.radians(target["angle"])

        x = int(
            CENTER[0] +
            target["distance"] * math.cos(angle_rad)
        )

        y = int(
            CENTER[1] +
            target["distance"] * math.sin(angle_rad)
        )

        # Draw target
        cv2.circle(
            radar,
            (x, y),
            7,
            (0, 255, 0),
            -1
        )

    # Title
    cv2.putText(
        radar,
        "DEFENCE RADAR SIMULATOR",
        (170, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Status
    cv2.putText(
        radar,
        "STATUS: ONLINE",
        (20, 680),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.putText(
        radar,
        f"TARGETS: {len(targets)}",
        (520, 680),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # Show radar
    cv2.imshow("Defence Radar", radar)

    # Press Q to quit
    key = cv2.waitKey(30) & 0xFF

    if key == ord("q"):
        break


cv2.destroyAllWindows()