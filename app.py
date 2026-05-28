from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

MODEL_PATH = "best.pt"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("best.pt not found. Put best.pt in the same folder as app.py")

model = YOLO(MODEL_PATH)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({
                "message": "No image received",
                "danger": False
            }), 400

        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)

        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({
                "message": "Invalid image",
                "danger": False
            }), 400

        results = model(frame, imgsz=320, conf=0.5)

        detected_objects = []
        danger_detected = False

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]

                if confidence > 0.5:
                    detected_objects.append(class_name)

                    if class_id == 2:
                        danger_detected = True

        if danger_detected:
            message = "DANGER DANGER"
            danger = True
        elif detected_objects:
            message = "Detected: " + ", ".join(set(detected_objects))
            danger = False
        else:
            message = "Nothing detected"
            danger = False

        return jsonify({
            "message": message,
            "danger": danger
        })

    except Exception as e:
        print("Detection error:", str(e), flush=True)

        return jsonify({
            "message": "Detection error: " + str(e),
            "danger": False
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)