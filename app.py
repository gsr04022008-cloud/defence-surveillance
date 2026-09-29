from flask import (
    Flask,
    jsonify,
    render_template,
    Response,
    send_file,
    request,
    redirect,
    url_for,
    session
)

import random
import cv2
import csv
import io

from datetime import datetime

from database import (
    create_database,
    save_detection,
    get_recent_logs
)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

# Demo secret key for local college project
app.secret_key = "defence-surveillance-demo-key"


create_database()


# =========================================================
# DEMO LOGIN DETAILS
# =========================================================

USERNAME = "admin"
PASSWORD = "admin123"


# =========================================================
# CAMERA
# =========================================================

camera = cv2.VideoCapture(0)

background = cv2.createBackgroundSubtractorMOG2(
    history=300,
    varThreshold=40,
    detectShadows=True
)


active_alerts = []


# =========================================================
# LOGIN REQUIRED FUNCTION
# =========================================================

def login_required():

    if "logged_in" not in session:

        return False

    return session["logged_in"] is True


# =========================================================
# LOGIN PAGE
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form.get("username", "")

        password = request.form.get("password", "")

        if (
            username == USERNAME
            and password == PASSWORD
        ):

            session["logged_in"] = True

            session["username"] = username

            return redirect(
                url_for("home")
            )

        else:

            error = "Invalid username or password."

    return render_template(
        "login.html",
        error=error
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# CAMERA FRAME GENERATOR
# =========================================================

def generate_camera_frames():

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame = cv2.resize(
            frame,
            (800, 500)
        )

        mask = background.apply(frame)

        mask = cv2.medianBlur(
            mask,
            5
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        object_count = 0

        for contour in contours:

            area = cv2.contourArea(
                contour
            )

            if area < 1500:
                continue

            x, y, w, h = cv2.boundingRect(
                contour
            )

            object_count += 1

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "OBJECT " + str(object_count),
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            "SURVEILLANCE CAMERA",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Objects: " + str(object_count),
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        success, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


# =========================================================
# SIMULATED TARGET GENERATOR
# =========================================================

def generate_targets():

    targets = []

    for i in range(1, 9):

        distance = random.randint(
            100,
            1500
        )

        speed = random.randint(
            5,
            100
        )

        angle = random.randint(
            0,
            360
        )

        if speed > 70:

            status = "ALERT"

            alert = {

                "target_id": i,

                "speed": speed,

                "distance": distance,

                "angle": angle,

                "time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            }

            active_alerts.append(
                alert
            )

        else:

            status = "NORMAL"

        target = {

            "id": i,

            "distance": distance,

            "speed": speed,

            "angle": angle,

            "status": status

        }

        targets.append(
            target
        )

        save_detection(
            target
        )

    if len(active_alerts) > 20:

        del active_alerts[:-20]

    return targets


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def home():

    if not login_required():

        return redirect(
            url_for("login")
        )

    return render_template(
        "index.html"
    )

@app.route("/about")
def about():

    if not login_required():

        return redirect(
            url_for("login")
        )

    return render_template(
        "about.html"
    )

# =========================================================
# TARGET API
# =========================================================

@app.route("/api/targets")
def targets():

    if not login_required():

        return jsonify({
            "error": "Login required"
        }), 401

    return jsonify(
        generate_targets()
    )


# =========================================================
# HISTORY API
# =========================================================

@app.route("/api/history")
def history():

    if not login_required():

        return jsonify({
            "error": "Login required"
        }), 401

    logs = get_recent_logs(50)

    result = []

    for log in logs:

        result.append({

            "database_id": log[0],

            "target_id": log[1],

            "distance": log[2],

            "speed": log[3],

            "angle": log[4],

            "status": log[5],

            "time": log[6]

        })

    return jsonify(result)


# =========================================================
# STATISTICS API
# =========================================================

@app.route("/api/statistics")
def statistics():

    if not login_required():

        return jsonify({
            "error": "Login required"
        }), 401

    logs = get_recent_logs(100)

    total = len(logs)

    normal = 0

    alerts = 0

    speeds = []

    distances = []

    for log in logs:

        speed = log[3]

        distance = log[2]

        status = log[5]

        speeds.append(
            speed
        )

        distances.append(
            distance
        )

        if status == "ALERT":

            alerts += 1

        else:

            normal += 1

    if total > 0:

        average_speed = (
            sum(speeds) / total
        )

        maximum_speed = max(
            speeds
        )

        average_distance = (
            sum(distances) / total
        )

    else:

        average_speed = 0

        maximum_speed = 0

        average_distance = 0

    return {

        "total_detections": total,

        "normal_detections": normal,

        "alert_detections": alerts,

        "average_speed": round(
            average_speed,
            2
        ),

        "maximum_speed": maximum_speed,

        "average_distance": round(
            average_distance,
            2
        )

    }


# =========================================================
# CAMERA ROUTE
# =========================================================

@app.route("/camera")
def camera_feed():

    if not login_required():

        return "Login required", 401

    return Response(

        generate_camera_frames(),

        mimetype=
        "multipart/x-mixed-replace; boundary=frame"

    )


# =========================================================
# ALERT API
# =========================================================

@app.route("/api/alerts")
def get_alerts():

    if not login_required():

        return jsonify({
            "error": "Login required"
        }), 401

    return jsonify(
        active_alerts
    )


# =========================================================
# CLEAR ALERTS
# =========================================================

@app.route(
    "/api/alerts/clear",
    methods=["POST"]
)
def clear_alerts():

    if not login_required():

        return jsonify({
            "error": "Login required"
        }), 401

    active_alerts.clear()

    return jsonify({

        "success": True,

        "message":
        "Alerts cleared"

    })


# =========================================================
# CSV EXPORT
# =========================================================

@app.route("/export/csv")
def export_csv():

    if not login_required():

        return redirect(
            url_for("login")
        )

    logs = get_recent_logs(
        500
    )

    output = io.StringIO()

    writer = csv.writer(
        output
    )

    writer.writerow([

        "Database ID",

        "Target ID",

        "Distance (m)",

        "Speed (m/s)",

        "Angle (degrees)",

        "Status",

        "Detected At"

    ])

    for log in logs:

        writer.writerow([

            log[0],

            log[1],

            log[2],

            log[3],

            log[4],

            log[5],

            log[6]

        ])

    output.seek(0)

    filename = (

        "defence_surveillance_report_"

        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        + ".csv"

    )

    return send_file(

        io.BytesIO(
            output.getvalue().encode(
                "utf-8"
            )
        ),

        mimetype="text/csv",

        as_attachment=True,

        download_name=filename

    )


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("=" * 50)

    print(
        "DEFENCE SURVEILLANCE SYSTEM"
    )

    print("=" * 50)

    print(
        "Database : ONLINE"
    )

    print(
        "Radar    : SIMULATED"
    )

    print(
        "Tracking : ONLINE"
    )

    print(
        "History  : ONLINE"
    )

    print(
        "Camera   : ONLINE"
    )

    print(
        "Alerts   : ONLINE"
    )

    print(
        "CSV      : ONLINE"
    )

    print(
        "Login    : ONLINE"
    )

    print()

    print(
        "Dashboard:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "Demo username: admin"
    )

    print(
        "Demo password: admin123"
    )

    print()

    app.run(
        debug=True,
        threaded=True
    )