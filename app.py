import cv2
import pandas as pd
from datetime import datetime
import os
import time

# Hide TensorFlow messages
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from deepface import DeepFace

# ---------------- SETUP ----------------

DATASET_PATH = "dataset"
ATTENDANCE_FILE = "attendance/attendance.csv"
PHOTO_FOLDER = os.path.join("attendance", "Photos")

os.makedirs(PHOTO_FOLDER, exist_ok=True)

# Create CSV if not exists
if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(
        columns=["Name", "Date", "Month", "Year", "Time", "Photo"]
    )
    df.to_csv(ATTENDANCE_FILE, index=False)

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- ATTENDANCE FUNCTION ----------------

def mark_attendance(name, frame):

    now = datetime.now()

    date = now.strftime("%d-%m-%Y")
    month = now.strftime("%B")
    year = now.strftime("%Y")
    current_time = now.strftime("%H:%M:%S")

    # Build photo filename + path (used only if we actually mark attendance)
    photo_name = f"{name}_{date}_{current_time.replace(':', '-')}.jpg"
    photo_path = os.path.join(PHOTO_FOLDER, photo_name)

    try:
        df = pd.read_csv(ATTENDANCE_FILE)
    except Exception:
        df = pd.DataFrame(
            columns=["Name", "Date", "Month", "Year", "Time", "Photo"]
        )

    already_marked = (
        (df["Name"] == name) & (df["Date"] == date)
    ).any()

    if not already_marked:

        # Save attendance photo ONLY once, only when marking for the first time today
        cv2.imwrite(photo_path, frame)

        new_row = {
            "Name": name,
            "Date": date,
            "Month": month,
            "Year": year,
            "Time": current_time,
            "Photo": photo_name,
        }

        df = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )

        df.to_csv(ATTENDANCE_FILE, index=False)

        print(f"✅ Attendance Marked : {name}")

        return "Attendance Marked"

    else:
        print(f"⚠ Already Marked Today : {name}")
        return "Already Marked"


# ---------------- CAMERA ----------------

cap = cv2.VideoCapture(0)

print("🔥 Face Attendance Started")
print("Press ESC to Exit")

last_check = 0
display_text = "Show Face"

# ---------------- LOOP ----------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    # Draw green box
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    current_time = time.time()

    # Run recognition every 3 seconds
    if len(faces) > 0 and current_time - last_check > 3:

        last_check = current_time

        try:
            result = DeepFace.find(
                img_path=frame,
                db_path=DATASET_PATH,
                enforce_detection=False,
                silent=True
            )

            if len(result) > 0 and len(result[0]) > 0:

                path = result[0].iloc[0]["identity"]
                name = os.path.splitext(os.path.basename(path))[0]

                # Pass the current frame so the photo can be saved
                status = mark_attendance(name, frame)

                display_text = f"{name} - {status}"

            else:
                display_text = "Unknown"

        except Exception as e:
            print("ERROR:", e)
            display_text = "Face Not Recognized"

    elif len(faces) == 0:
        display_text = "No Face Detected"

    cv2.putText(
        frame,
        display_text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()