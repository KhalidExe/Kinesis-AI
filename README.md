# 🖐️ Kinesis-AI | كينيسيس

![Project Status](https://img.shields.io/badge/Status-Alpha_v0.1.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10_Required-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-0099CC?style=for-the-badge&logo=google&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

> **Touchless System Control using Computer Vision.**
> Kinesis-AI utilizes Google's MediaPipe to transform your hand gestures into powerful system commands, allowing you to control volume and playback speed without touching the keyboard.

---

## ⚠️ Important Note (Read First)
**This project requires Python 3.10 to function correctly.**
Newer versions (like Python 3.13) are currently incompatible with MediaPipe dependencies. Please ensure you have Python 3.10 installed before running.

---

## 📸 Demo
*(GIFs and Screenshots coming in v0.2.0...)*

---

## ⚡ Key Features

### 👁️ AI-Powered Vision
- **Real-Time Tracking:** 🚀 High-performance hand detection running at 30+ FPS.
- **21-Point Skeleton:** Precision tracking of finger joints and palm orientation.
- **Dual Hand Support:** Intelligently distinguishes between Right and Left hands for different controls.

### 🎛️ System Control (Roadmap)
- **Volume Master:** 🔊 Pinch your **Right Hand** fingers to adjust system volume smoothly.
- **Speed Commander:** ⏩ Pinch your **Left Hand** fingers to control video playback speed (YouTube/VLC).

### 🛠️ Engineering
- **Privacy First:** All processing happens locally on your machine. No cloud data.
- **Optimized:** Lightweight code designed to run in the background with minimal CPU usage.

---

## 🛠️ Tech Stack

* **Core:** Python 3.10.
* **Computer Vision:** OpenCV, MediaPipe (v0.10.9).
* **System Automation:** PyCaw (Audio), PyAutoGUI (Inputs).
* **Math:** NumPy.

---

## 🚀 How to Run (Locally)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/KhalidExe/Kinesis-AI.git](https://github.com/KhalidExe/Kinesis-AI.git)
    cd Kinesis-AI
    ```

2.  **Set up Environment (Critical Step):**
    *Make sure you have Python 3.10 installed.*
    ```bash
    # Create virtual environment using Python 3.10
    py -3.10 -m venv venv
    
    # Activate it (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the AI:**
    ```bash
    python main.py
    ```
    *Press 'q' on the keyboard to exit the application.*

---

## 📂 Project Structure

```text
Kinesis-AI/
│
├── main.py              # The Brain: Main Loop & Vision Logic
├── requirements.txt     # Locked Dependencies (Stable)
├── README.md            # Documentation
│
└── venv/                # Virtual Environment (Excluded from Git)
```

## 🔮 Future Roadmap
- [x] v0.1.0: Core Skeleton Tracking & Environment Setup.

- [ ] v0.2.0: Right Hand Volume Control (PyCaw Integration).

- [ ] v0.3.0: Left Hand Playback Speed Control.

- [ ] v1.0.0: Visual HUD & Sci-Fi UI Overlay.

*Developed by **KhalidExe** © 2026*