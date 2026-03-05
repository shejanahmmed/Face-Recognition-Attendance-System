# Face Recognition Attendance System

A real-time face recognition-based attendance system developed with Python, OpenCV, and the `face_recognition` library. This system detects and identifies faces through a webcam, matching them against known images, and automatically logs attendance into a CSV file.

## Features

- **Real-time Face Detection:** Efficiently detects faces in a live video stream.
- **Accurate Recognition:** Uses deep learning-based face encodings for high-accuracy identification.
- **Automated Attendance Logging:** Records the name and timestamp of recognized individuals.
- **CSV Data Export:** Attendance data is saved daily in `.csv` format for easy integration and analysis.
- **User-Friendly Interface:** Provides visual feedback (on-screen labels) during the recognition process.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x**
- **CMake** (required for `dlib` installation)
- **C++ Compiler** (Visual Studio with C++ development tools on Windows, or GCC/G++ on Linux/macOS)

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/Face-Recognition-Attendance-System.git
    cd Face-Recognition-Attendance-System
    ```

2.  **Install Required Libraries:**
    Install the core dependencies using `pip`:
    ```bash
    pip install cmake
    pip install face_recognition
    pip install opencv-python
    pip install numpy
    ```

3.  **Prepare Reference Images:**
    Place the `.jpg` or `.png` images of individuals you wish to recognize in the `faces/` directory. Ensure the filename corresponds to the person's name (e.g., `shejan.jpg`, `tarikul.jpg`).

## Usage

1.  **Run the System:**
    ```bash
    python main.py
    ```

2.  **Operation:**
    - The webcam will open and begin scanning for faces.
    - Recognized individuals will see their name displayed with "Present" on the screen.
    - Their attendance (Name, Time) will be recorded in a CSV file named `DD-MM-YYYY.csv`.
    - **Press 'q'** to quit the application.

## Project Structure

```text
Face-Recognition-Attendance-System/
├── faces/                   # Directory containing reference images
│   ├── shejan.jpg
│   └── tarikul.jpg
├── face_recognition_models/  # (Optional) Pre-trained models
├── main.py                  # Core application logic
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

## How It Works

1.  **Loading:** The system loads images from the `faces/` directory and generates face encodings (128-dimensional vectors) for each.
2.  **Detection:** The webcam captures frames, which are then resized and converted to RGB.
3.  **Matching:** Detected face encodings from the live stream are compared against the known encodings using Euclidean distance.
4.  **Logging:** If a match is found and the person hasn't been marked present yet, their name and current time are written to the daily CSV file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [face_recognition library](https://github.com/ageitgey/face_recognition) by Adam Geitgey.
- [OpenCV](https://opencv.org/) for computer vision processing.
