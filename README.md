# Face-Tracking Laser Turret

A real-time **face-tracking Arduino turret** that uses a webcam and OpenCV to detect a person’s head and aim a low-power laser precisely at that point.




---

## Overview
- **Detection**: A Python program captures webcam video and locates the head/face using OpenCV.
- **Coordinate Mapping**: The program sends the face center `(x, y)` over a USB serial link to the Arduino UNO.
- **Actuation**: Two SG90 servos (pan & tilt) move the turret so the laser continuously follows the detected head.

---

## Hardware
- Arduino UNO (or compatible)
- 2 × SG90 (or similar) micro-servo motors
- Low-power red laser diode or LED with current-limiting resistor
- External 5 V supply (e.g., 3 × AAA battery pack) for the servos
- Breadboard and jumper wires
- Webcam connected to the host computer

> **Safety**  
> Use only a **low-power (Class 1 or Class 2) laser**.  
> Never point at eyes or reflective surfaces.

---


## Software Setup

### 1️⃣ Python / OpenCV
1. Open Face_Tracking_Code.py in VS Code and run it.

### 2️⃣ Arduino
1. Open **`Arduino_IDE_Code.ino`** in the Arduino IDE.
2. Select **Board: Arduino UNO** and the correct **Port**.
3. Upload the sketch.  
   *The code reads serial input, maps coordinates to servo angles, and toggles the laser.*





⚠️ **Note:** This video file is too large to display on GitHub. Click **View raw** in project_video.mov to download it.
