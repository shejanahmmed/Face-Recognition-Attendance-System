import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime

# Load reference images
def load_face_encoding(image_path):
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return None
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        print(f"[WARNING] No face found in image: {image_path}")
        return None
    return encodings[0]

# Initialize camera
video_capture = cv2.VideoCapture(0)

# Load known faces
tarikul_encoding = load_face_encoding("faces/tarikul.jpg")
shejan_encoding = load_face_encoding("faces/shejan.jpg")

known_face_encodings = []
known_face_names = []

if tarikul_encoding is not None:
    known_face_encodings.append(tarikul_encoding)
    known_face_names.append("Tarikul")

if shejan_encoding is not None:
    known_face_encodings.append(shejan_encoding)
    known_face_names.append("Shejan")

students = known_face_names.copy()

now = datetime.now()
current_date = now.strftime("%d-%m-%Y")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("[ERROR] Failed to grab frame from webcam.")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)

        name = "Unknown"
        if len(face_distance) > 0:
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name + " Present", (10, 100), font, 1.5, (255, 0, 0), 3)

        # Save attendance
        if name in students:
            students.remove(name)
            current_time = now.strftime("%H:%M:%S")
            lnwriter.writerow([name, current_time])

    cv2.imshow("Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
