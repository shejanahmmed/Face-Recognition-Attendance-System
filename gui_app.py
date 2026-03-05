import customtkinter as ctk
import cv2
from PIL import Image
from face_recognition_handler import FaceRecognitionHandler
import threading
import traceback
import tkinter.messagebox as messagebox

class AttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Setup Window ---
        self.title("Face Recognition Attendance System Pro")
        self.geometry("1100x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Initialize Face Recognition ---
        self.face_handler = FaceRecognitionHandler()
        self.video_running = False
        self.current_img_tk = None

        # --- Grid Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Attendance Pro", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- Stats Section ---
        self.stats_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.total_label = ctk.CTkLabel(self.stats_frame, text="Total Students: 0", font=ctk.CTkFont(size=14))
        self.total_label.grid(row=0, column=0, sticky="w", pady=5)

        self.present_label = ctk.CTkLabel(self.stats_frame, text="Present: 0", font=ctk.CTkFont(size=14, weight="bold"), text_color="#4CAF50")
        self.present_label.grid(row=1, column=0, sticky="w", pady=5)

        self.absent_label = ctk.CTkLabel(self.stats_frame, text="Absent: 0", font=ctk.CTkFont(size=14), text_color="#FF5252")
        self.absent_label.grid(row=2, column=0, sticky="w", pady=5)

        # --- Control Buttons ---
        self.start_btn = ctk.CTkButton(self.sidebar_frame, text="Start Scanner", command=self.toggle_video, fg_color="#1a73e8")
        self.start_btn.grid(row=2, column=0, padx=20, pady=10)

        self.export_btn = ctk.CTkButton(self.sidebar_frame, text="Export PDF Report", command=self.export_pdf, fg_color="#27ae60", hover_color="#219150")
        self.export_btn.grid(row=3, column=0, padx=20, pady=10)

        self.quit_btn = ctk.CTkButton(self.sidebar_frame, text="Exit Application", command=self.destroy, fg_color="#c62828", hover_color="#b71c1c")
        self.quit_btn.grid(row=4, column=0, padx=20, pady=10)

        # --- Main Video Area ---
        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)

        self.video_label = ctk.CTkLabel(self.main_content, text="Webcam Offline\nPress 'Start Scanner' to Begin", font=ctk.CTkFont(size=18))
        self.video_label.grid(row=0, column=0, sticky="nsew")

        # Start background stats update
        self.update_stats()

    def update_stats(self):
        """Periodically update the statistics on the UI."""
        stats = self.face_handler.get_stats()
        self.total_label.configure(text=f"Total Registered: {stats['total']}")
        self.present_label.configure(text=f"Present Today: {stats['present']}")
        self.absent_label.configure(text=f"Absent: {stats['absent']}")
        self.after(2000, self.update_stats)

    def export_pdf(self):
        """Trigger PDF export and show status message."""
        success, message = self.face_handler.export_to_pdf()
        if success:
            messagebox.showinfo("Export Successful", f"PDF Report generated: {message}")
        else:
            messagebox.showerror("Export Failed", message)

    def toggle_video(self):
        """Start or stop the video feed."""
        if not self.video_running:
            self.video_capture = cv2.VideoCapture(0)
            if not self.video_capture.isOpened():
                self.video_label.configure(text="Error: Could not open webcam.")
                return
            
            self.video_running = True
            self.start_btn.configure(text="Stop Scanner", fg_color="#e67e22")
            threading.Thread(target=self.video_loop, daemon=True).start()
        else:
            self.video_running = False
            self.start_btn.configure(text="Start Scanner", fg_color="#1a73e8")
            if hasattr(self, 'video_capture'):
                self.video_capture.release()
            self.video_label.configure(text="Webcam Offline", image=None)

    def update_video_label(self, img):
        """Update the video label with a new frame. Must be called from main thread."""
        if self.video_running:
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            self.video_label.configure(image=ctk_img, text="")
            self.video_label._image = ctk_img 

    def video_loop(self):
        """Background thread for processing frames and updating the UI."""
        try:
            while self.video_running:
                ret, frame = self.video_capture.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                results = self.face_handler.process_frame(frame)

                for person in results:
                    (top, right, bottom, left) = person['location']
                    name = person['name']
                    color = (46, 204, 113) if name != "Unknown" else (219, 152, 52) 
                    
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2_image)
                img = self.resize_image(img, 800, 600)
                self.after(0, self.update_video_label, img)
                
        except Exception as e:
            print(f"Error in video loop: {e}")
            traceback.print_exc()
        finally:
            if hasattr(self, 'video_capture'):
                self.video_capture.release()

    def resize_image(self, img, max_width, max_height):
        """Resizes the image to fit within the specified dimensions."""
        width, height = img.size
        aspect_ratio = width / height
        
        if width > max_width:
            width = max_width
            height = int(width / aspect_ratio)
        
        if height > max_height:
            height = max_height
            width = int(height * aspect_ratio)
            
        return img.resize((width, height), Image.Resampling.LANCZOS)

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()
