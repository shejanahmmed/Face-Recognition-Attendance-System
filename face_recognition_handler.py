import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import csv
from fpdf import FPDF

class FaceRecognitionHandler:
    def __init__(self, faces_dir="faces"):
        self.faces_dir = faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.students = []
        self.current_date = datetime.now().strftime("%d-%m-%Y")
        self.csv_file = f"{self.current_date}.csv"
        self._load_known_faces()

    def _load_known_faces(self):
        """Load all images from the faces directory and encode them."""
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
            
        for filename in os.listdir(self.faces_dir):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                path = os.path.join(self.faces_dir, filename)
                name = os.path.splitext(filename)[0].capitalize()
                
                try:
                    image = face_recognition.load_image_file(path)
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_names.append(name)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        self.students = self.known_face_names.copy()

    def process_frame(self, frame):
        """Detect and recognize faces in a single frame."""
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        results = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            name = "Unknown"
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            results.append({
                "name": name,
                "location": (top, right, bottom, left)
            })
            
            if name in self.students:
                self.students.remove(name)
                self._log_attendance(name)
                
        return results

    def _log_attendance(self, name):
        """Write recognized name and time to CSV."""
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        file_exists = os.path.isfile(self.csv_file)
        
        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Name", "Time"])
            writer.writerow([name, current_time])

    def get_stats(self):
        """Return basic statistics for the UI."""
        total = len(self.known_face_names)
        present = total - len(self.students)
        return {
            "total": total,
            "present": present,
            "absent": len(self.students)
        }

    def export_to_pdf(self):
        """Converts the current day's CSV attendance to a professional PDF report."""
        if not os.path.exists(self.csv_file):
            return False, "No attendance recorded yet today."

        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Daily Attendance Report", ln=True, align="C")
            
            # Date
            pdf.set_font("Arial", "", 12)
            pdf.cell(200, 10, txt=f"Date: {self.current_date}", ln=True, align="C")
            pdf.ln(10)

            # Table Header
            pdf.set_fill_color(200, 220, 255)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(95, 10, "Name", 1, 0, "C", True)
            pdf.cell(95, 10, "Arrival Time", 1, 1, "C", True)

            # Table Body
            pdf.set_font("Arial", "", 12)
            with open(self.csv_file, "r") as f:
                reader = csv.reader(f)
                next(reader) # Skip header
                for row in reader:
                    pdf.cell(95, 10, row[0], 1, 0, "C")
                    pdf.cell(95, 10, row[1], 1, 1, "C")

            pdf_filename = f"Attendance_{self.current_date}.pdf"
            pdf.output(pdf_filename)
            return True, pdf_filename
        except Exception as e:
            return False, str(e)
