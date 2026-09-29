import cv2


print("=" * 50)
print("CAMERA SURVEILLANCE MODULE")
print("=" * 50)

print("Starting camera...")
print("Press Q to quit.")


camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print("ERROR: Could not open camera.")
    exit()


background = cv2.createBackgroundSubtractorMOG2(
    history=300,
    varThreshold=40,
    detectShadows=True
)


while True:

    success, frame = camera.read()

    if not success:

        print("Could not read camera frame.")
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

        area = cv2.contourArea(contour)


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


    cv2.putText(
        frame,
        "Press Q to Exit",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.imshow(
        "Defence Surveillance Camera",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


camera.release()

cv2.destroyAllWindows()

print("Camera module stopped.")