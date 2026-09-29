import sqlite3
from datetime import datetime

DATABASE = "defence_system.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detection_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,
            distance REAL,
            speed REAL,
            angle REAL,
            status TEXT,
            detected_at TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Database ready.")


def save_detection(target):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO detection_logs
        (target_id, distance, speed, angle, status, detected_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        target["id"],
        target["distance"],
        target["speed"],
        target["angle"],
        target["status"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_recent_logs(limit=20):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            target_id,
            distance,
            speed,
            angle,
            status,
            detected_at
        FROM detection_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    logs = cursor.fetchall()

    connection.close()

    return logs


if __name__ == "__main__":
    create_database()