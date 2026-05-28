from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Put best.pt in the same folder as app.py
model = YOLO("best.pt")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    try:
        data = request.json["image"]

        image_data = data.split(",")[1]
        image_bytes = base64.b64decode(image_data)

        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        results = model(frame)

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

        # YOLO draws bounding boxes automatically
        annotated_frame = results[0].plot()

        _, buffer = cv2.imencode(".jpg", annotated_frame)
        processed_image = base64.b64encode(buffer).decode("utf-8")

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
            "danger": danger,
            "image": processed_image
        })

    except Exception as e:
        print("Detection error:", e)
        return jsonify({
            "message": "Detection error",
            "danger": False,
            "image": None
        })


if __name__ == "__main__":
    app.run(debug=True)