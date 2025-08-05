# 🔥 Fire Sentinel

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Arduino](https://img.shields.io/badge/Arduino-UNO-green?logo=arduino)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-red?logo=ultralytics)

A real-time fire detection and automatic suppression system using YOLOv8, Arduino, and WhatsApp alerts.

---

## 📸 Overview

**Fire Sentinel** is an intelligent fire detection system that:
- Detects fire using YOLOv8 and an IP camera.
- Rotates to scan the environment using a 360° servo motor.
- Sends real-time fire alerts via WhatsApp (with image proof).
- Activates a buzzer and pushes a CO₂ nozzle on confirmed fire detection.

---

## 🛠️ Technologies Used

- Python 3
- OpenCV, Ultralytics YOLOv8
- PyWhatKit (WhatsApp API)
- Arduino UNO
- IP Camera (or mobile IP webcam)

---

## ⚙️ Setup Guide

1. **Clone the repository**:
    ```bash
    git clone https://github.com/404-aniket/fire-sentinel.git
    cd fire-sentinel
    ```

2. **Install Python dependencies manually**:
    ```bash
    pip install opencv-python ultralytics pywhatkit
    ```
3. **Prepare Hardware**:
    - Upload `ARDUINO_CODE_FOR_FIRE-SENTINAL.ino` to Arduino.
    - Wire up LEDs, buzzer, and servos according to the code.

4. **Edit Python Script**:
    - Set your IP camera URL.
    - Update your phone number in `Fire_Sentinel_Without_PC_Alarm.py`.

5. **Run the Fire Sentinel**:
    ```bash
    python Fire_Sentinel_Without_PC_Alarm.py
    ```

---

## 🤖 Arduino Role

- Receives commands (`ROTATE`, `STOP`, `FIRE`, `RESUME`) via serial.
- Controls servo motors for scanning and nozzle activation.
- Handles LED indicators and buzzer alerts.

---

## 🧠 Python Role

- Captures live video feed from IP camera.
- Detects fire using YOLOv8 model.
- Calculates fire distance and triggers Arduino actions.
- Sends WhatsApp alerts with fire images automatically.

## 🤝 Authors 

- [404-aniket](https://github.com/404-aniket)
- [Shruti](https://github.com/shruti16-code) <!-- Replace "username" with Shruti's GitHub username -->

