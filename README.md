# LPG Knob & Flame Detector

A Flask-based real-time LPG safety monitoring system using YOLO object detection and live camera input.

This project helps detect:

* LPG stove knob states
* Flame presence
* Potential danger situations

The application uses:

* Flask
* YOLO (`best.pt`)
* OpenCV
* JavaScript camera streaming

---

# Features

* Live webcam monitoring
* Real-time object detection using YOLO
* Mobile camera support
* Danger alert system
* Flask backend API
* Responsive frontend UI

---

# Tech Stack

## Backend

* Python
* Flask
* Ultralytics YOLO
* OpenCV

## Frontend

* HTML
* CSS
* JavaScript

---

# Project Structure

```text
project/
│
├── app.py
├── best.pt
├── requirements.txt
├── Procfile
│
├── templates/
│   └── index.html
|   ├── base.html
│
├── static/
│   ├── css/
│   │   └── main.css
│   │
│   └── images/
│       └── flamebackground.webp
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/puranik1406/LPG-Stove-Knob-Flame-Detection-WebApp.git
cd LPG-Stove-Knob-Flame-Detection-WebApp
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Locally

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Model

Place trained YOLO model file:

```text
best.pt
```

inside the project root directory.

Example:

```python
model = YOLO("best.pt")
```

---


# Important Notes

* Browser camera access works only on:

  * `localhost`
  * `https://`

* Webcam alone cannot detect invisible LPG gas leakage.

* For real gas leakage detection, hardware gas sensors such as MQ-2 or MQ-5 are required.
---

# License

MIT License
