import random
import time


class Target:
    def __init__(self, target_id):
        self.id = target_id
        self.distance = random.randint(100, 1000)
        self.speed = random.randint(5, 50)
        self.angle = random.randint(0, 360)
        self.status = "NORMAL"

    def update(self):
        # Simulate movement
        self.distance += random.randint(-20, 20)
        self.speed += random.randint(-3, 3)

        # Keep values realistic for the simulator
        self.distance = max(50, min(self.distance, 1500))
        self.speed = max(1, min(self.speed, 100))

        # Simulation rule for an alert
        if self.speed > 70:
            self.status = "ALERT"
        else:
            self.status = "NORMAL"

    def display(self):
        print(
            f"Target {self.id} | "
            f"Distance: {self.distance} m | "
            f"Speed: {self.speed} m/s | "
            f"Angle: {self.angle}° | "
            f"Status: {self.status}"
        )


targets = [Target(i) for i in range(1, 6)]

print("=" * 75)
print("             TARGET TRACKING SIMULATOR")
print("=" * 75)

for cycle in range(10):

    print(f"\n--- Scan {cycle + 1} ---")

    alert_count = 0

    for target in targets:
        target.update()
        target.display()

        if target.status == "ALERT":
            alert_count += 1

    print(f"\nActive Alerts: {alert_count}")

    time.sleep(1)

print("\nSimulation completed.")