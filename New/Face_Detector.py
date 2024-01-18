from ultralytics import YOLO
import cv2
import os
import numpy as np

model_detection = YOLO("yolov8n-face.pt")

def detect_save_face(image_path, is_voice):

    image = cv2.imread(image_path)
    results_detection = model_detection.predict(source=image, show=False)

    max_confidence = 0
    best_faces = []

    for result in results_detection:
        boxes = result.boxes.xyxy.cpu().numpy()  # Convert to NumPy array
        probs = result.boxes.conf.cpu().numpy()  # Convert to NumPy array

        for box, prob in zip(boxes, probs):
            confidence = prob.item()
            if confidence > max_confidence:
                max_confidence = confidence
                best_faces = [box]
            elif confidence == max_confidence:
                best_faces.append(box)

    if best_faces:
        # Save individual cropped faces as rectangles in black and white
        for i, face_box in enumerate(best_faces):
            xmin, ymin, xmax, ymax = map(int, face_box)

            # Calculate the length of the longer side
            side_length = max(xmax - xmin, ymax - ymin)

            # Adjust the coordinates to crop a square region with the length of the longer side
            center_x, center_y = (xmin + xmax) // 2, (ymin + ymax) // 2
            xmin = max(0, center_x - side_length // 2)
            ymin = max(0, center_y - side_length // 2)
            xmax = min(image.shape[1], center_x + side_length // 2)
            ymax = min(image.shape[0], center_y + side_length // 2)

            cropped_face = image[ymin:ymax, xmin:xmax]
            cropped_face_gray = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)

            if is_voice:
                filename = f"best_face_voice.png"
            else:
                filename = f"best_face_camera.png"

            cv2.imwrite(filename, cropped_face_gray)
            print(f"Best face saved as '{filename}'")