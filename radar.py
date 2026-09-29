import random
import math
import time


def generate_target(target_id):
    distance = random.randint(100, 1000)
    angle = random.randint(0, 360)
    speed = random.randint(5, 50)

    x = distance * math.cos(math.radians(angle))
    y = distance * math.sin(math.radians(angle))

    return {
        "id": target_id,
        "distance": distance,
        "angle": angle,
        "speed": speed,
        "x": round(x, 2),
        "y": round(y, 2)
    }


def display_target(target):
    print("-" * 45)
    print(f"Target ID : {target['id']}")
    print(f"Distance  : {target['distance']} m")
    print(f"Angle     : {target['angle']}°")
    print(f"Speed     : {target['speed']} m/s")
    print(f"Position  : X={target['x']} m, Y={target['y']} m")


print("=" * 45)
print("       DEFENCE RADAR SIMULATOR")
print("=" * 45)

for i in range(1, 6):
    target = generate_target(i)
    display_target(target)
    time.sleep(1)

print("-" * 45)
print("Radar simulation completed.")