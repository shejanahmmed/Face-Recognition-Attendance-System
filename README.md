# 📸 Face Recognition Attendance System Pro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

A professional, real-time face recognition attendance system featuring a modern dark-themed Desktop GUI, live statistics, and automated PDF reporting. Optimized for **Visual Studio Code** users.

## 🚀 Features

- **🖥️ Modern GUI Dashboard:** Built with `CustomTkinter` for a sleek, dark-mode professional interface.
- **🔍 Real-time Recognition:** High-accuracy face detection and identification using deep learning encodings.
- **📊 Live Attendance Stats:** Dynamic sidebar showing Total Registered, Present, and Absent counts.
- **📄 Automated PDF Export:** Generate professional attendance reports with a single click.
- **🎨 Sleek Overlays:** Visual bounding boxes and status labels integrated into the live video feed.
- **🧩 Modular Architecture:** Clean separation between UI logic and face recognition processing.

## 🛠️ Prerequisites

- **🐍 Python 3.11+**
- **💻 Visual Studio Code** (Recommended Editor)

## 📦 Installation (Optimized for Windows/VS Code)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/Face-Recognition-Attendance-System.git
   cd Face-Recognition-Attendance-System
   ```

2. **Install Core Libraries:**
   ```bash
   pip install opencv-python numpy Pillow customtkinter fpdf
   ```

3. **Install Face Recognition (The Easy Way):**
   To avoid downloading heavy C++ Build Tools, use the pre-compiled version of dlib:
   ```bash
   pip install dlib-bin
   pip install face_recognition --no-deps
   pip install face_recognition_models
   ```

## 🎮 Usage

1. **Prepare Data:**
   Place reference images in the `faces/` directory (e.g., `shejan.jpg`, `tarikul.jpg`).

2. **Launch Application:**
   Open the terminal in VS Code and run:
   ```bash
   python gui_app.py
   ```
   *OR simply press **F5** in VS Code!*

3. **Operation:**
   - Click **"Start Scanner"** to begin real-time detection.
   - Click **"Export PDF Report"** to save today's attendance log as a professional PDF.

## 📂 Project Structure

```text
Face-Recognition-Attendance-System/
├── .vscode/                 # VS Code configurations (F5 to run)
├── backup/                  # Original script backup
├── faces/                   # Reference student images
├── face_recognition_handler.py # Core recognition logic & PDF generation
├── gui_app.py               # Modern CustomTkinter GUI application
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) - The world's simplest face recognition API.
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI library for Python.
- [OpenCV](https://opencv.org/) - Comprehensive computer vision tools.
