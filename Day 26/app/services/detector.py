# if you use pretrained model of yolov8n then use this code as below:

from ultralytics import YOLO
import numpy as np
import cv2

# YOLO DETECTOR

class Detector:

    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)

    def predict(self, image: np.ndarray, confidence: float = 0.25):
        results = self.model.predict(
            source=image,
            conf=confidence,
            verbose=False
        )

        detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                conf = float(box.conf[0])

                detections.append({
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": conf,
                    "bounding_box": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2
                    }
                })

        return detections, results

    def draw_predictions(self, image: np.ndarray, detections: list):
        annotated = image.copy()

        for det in detections:
            box = det["bounding_box"]
            x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
            label = f'{det["class_name"]} {det["confidence"]:.2f}'

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated,
                label,
                (x1, max(y1 - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        return annotated


# SINGLETON INSTANCE (this is what prediction.py imports)

detector = Detector()






# if you use trained model of helmet detection then use this code as below:


# import os

# from ultralytics import YOLO
# import numpy as np
# import cv2


# # MODEL PATH
# # detector.py lives at: Day 26/app/services/detector.py
# # best.pt lives at:      Day 26/models/best.pt
# # so go up 2 levels from services/ to reach Day 26/, then into models/

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "..", "..", "models", "best.pt")


# # YOLO DETECTOR

# class Detector:

#     def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
#         self.model = YOLO(model_path)

#     def predict(self, image: np.ndarray, confidence: float = 0.25):
#         results = self.model.predict(
#             source=image,
#             conf=confidence,
#             verbose=False
#         )

#         detections = []

#         for result in results:
#             for box in result.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 class_id = int(box.cls[0])
#                 class_name = self.model.names[class_id]
#                 conf = float(box.conf[0])

#                 detections.append({
#                     "class_id": class_id,
#                     "class_name": class_name,
#                     "confidence": conf,
#                     "bounding_box": {
#                         "x1": x1,
#                         "y1": y1,
#                         "x2": x2,
#                         "y2": y2
#                     }
#                 })

#         return detections, results

#     def draw_predictions(self, image: np.ndarray, detections: list):
#         annotated = image.copy()

#         for det in detections:
#             box = det["bounding_box"]
#             x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
#             label = f'{det["class_name"]} {det["confidence"]:.2f}'

#             cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(
#                 annotated,
#                 label,
#                 (x1, max(y1 - 10, 0)),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6,
#                 (0, 255, 0),
#                 2
#             )

#         return annotated


# # SINGLETON INSTANCE (this is what prediction.py imports)

# detector = Detector()