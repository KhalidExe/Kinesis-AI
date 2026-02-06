# 🖐️ Kinesis-AI | كينيسيس

![Project Status](https://img.shields.io/badge/Status-Dev_v0.3.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10_Required-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-0099CC?style=for-the-badge&logo=google&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

> **Touchless System Control using Computer Vision.**
> Kinesis-AI utilizes Google's MediaPipe to transform your hand gestures into powerful system commands. Now featuring "Smart Lock" to prevent accidental triggers.

---

## ⚠️ Important Note
**This project requires Python 3.10.**
Please ensure you are using the correct python version to avoid dependency conflicts.

---

## ⚡ Key Features

### 🔒 Smart Lock & Volume Control (Enhanced in v0.3.0)
- **Safety First:** The system ignores accidental gestures.
- **How to Activate:** **Fold your Pinky Finger** to unlock the controls.
- **Volume Control:** While unlocked, pinch your Thumb and Index to adjust volume.
- **Visual Feedback:** HUD turns **Green** when active, and **Red/Gray** when locked.

### 👁️ AI-Powered Vision
- **Real-Time Tracking:** High-performance hand detection (30+ FPS).
- **Sci-Fi Visuals:** Neon-style skeleton tracking with cyan joints and magenta connections.
- **Privacy First:** All processing happens locally on your machine.

---

## 🛠️ Tech Stack

* **Core:** Python 3.10.
* **Computer Vision:** OpenCV, MediaPipe (v0.10.9).
* **System Automation:** PyCaw (Audio Control), PyAutoGUI (Keyboard).
* **Math:** NumPy.

---

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/KhalidExe/Kinesis-AI.git](https://github.com/KhalidExe/Kinesis-AI.git)
    cd Kinesis-AI
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the AI:**
    ```bash
    python main.py
    ```

### 🎮 Controls Checklist:
1.  **Raise Right Hand.**
2.  **Fold Pinky Finger** (Hold it down to activate).
3.  **Pinch Thumb & Index** to change volume.

---

## 🔮 Future Roadmap

- [x] **v0.1.0:** Core Skeleton Tracking & Environment Setup.
- [x] **v0.2.0:** Right Hand Volume Control & Sci-Fi HUD.
- [ ] **v0.3.0:** Smart Lock & Left Hand Playback Speed Control (In Progress).
- [ ] **v1.0.0:** Full Virtual Dashboard Overlay.

---

*Developed by **KhalidExe** © 2026*