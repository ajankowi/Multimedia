from ultralytics import YOLO
import cv2
import os
import numpy as np

model_detection = YOLO("yolov8n-face.pt")

def detect_save_face(image_path, is_voice):

    image = cv2.imread(image_path)
    results_detection = model_detection.predict(source=image, show=False)

    max_confidence = 0
    best_face = None

    for result in results_detection:
        boxes = result.boxes.xyxy.cpu().numpy()  # Convert to NumPy array
        probs = result.boxes.conf.cpu().numpy()  # Convert to NumPy array

        for box, prob in zip(boxes, probs):
            confidence = prob.item()
            if confidence > max_confidence:
                max_confidence = confidence
                best_face = box

    if best_face is not None:
        xmin, ymin, xmax, ymax = map(int, best_face)

        xmin, xmax = max(0, xmin), min(image.shape[1], xmax)
        ymin, ymax = max(0, ymin), min(image.shape[0], ymax)

        cropped_face = image[ymin:ymax, xmin:xmax]

        if is_voice:
            filename = f"best_face_voice.png"
        else:
            filename = f"best_face_camera.png"

        cv2.imwrite(filename, cropped_face)
        print(f"Best face saved as '{filename}'")