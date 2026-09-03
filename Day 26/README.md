# Custom YOLO Prediction API

A REST API built with **FastAPI** to serve a custom-trained **YOLO object detection model**. The API allows users or other applications to upload an image, run YOLO inference, and receive object detection results in JSON format. It also provides an endpoint for returning the processed image with bounding boxes.

---

## Features

* Image upload
* Custom YOLO model inference
* Configurable confidence threshold
* JSON prediction response
* Detected class names
* Confidence scores
* Bounding box coordinates
* Detection count
* Processed image with bounding boxes
* Input image validation
* Proper HTTP error handling
* Interactive Swagger/OpenAPI documentation

---

## How FastAPI Connects with the YOLO Model

FastAPI acts as the backend layer between the client application and the trained YOLO model.

The API loads the trained YOLO model through a detector service. When an image is uploaded, FastAPI receives the image and passes it to the YOLO detector for inference.

The overall workflow is:

```text
Client
   |
   | Upload Image
   v
FastAPI
   |
   | Validate Image
   v
YOLO Detector
   |
   | Run Inference
   v
Predictions
   |
   +----> JSON Response
   |
   +----> Processed Image
```

The trained model is loaded once when the application starts, allowing the API to reuse the same model for incoming prediction requests.

---

## `/predict` Endpoint

The main prediction endpoint is:

```http
POST /predict
```

It accepts an image using multipart form-data.

The endpoint performs the following steps:

1. Receives the uploaded image.
2. Checks whether the uploaded file is a valid image.
3. Reads the image using OpenCV.
4. Sends the image to the custom YOLO model.
5. Applies the requested confidence threshold.
6. Extracts detected classes and confidence scores.
7. Extracts bounding box coordinates.
8. Counts the total detections.
9. Returns the prediction results as JSON.

---

## Request Format

The request uses `multipart/form-data`.

Example using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -F "file=@test.jpg" \
  -F "confidence=0.25"
```

### Parameters

| Parameter    | Type       | Description                                 |
| ------------ | ---------- | ------------------------------------------- |
| `file`       | Image File | Image to be analyzed                        |
| `confidence` | Float      | Minimum confidence threshold for detections |

For example:

```text
confidence = 0.25
```

means detections below 25% confidence are ignored.

---

## Response Format

The `/predict` endpoint returns a JSON response containing:

* Detection count
* Detected class
* Confidence score
* Bounding box coordinates

Example:

```json
{
  "detection_count": 2,
  "predictions": [
    {
      "class_name": "helmet",
      "confidence": 0.94,
      "bbox": {
        "x1": 120,
        "y1": 85,
        "x2": 310,
        "y2": 270
      }
    },
    {
      "class_name": "helmet",
      "confidence": 0.87,
      "bbox": {
        "x1": 350,
        "y1": 100,
        "x2": 520,
        "y2": 290
      }
    }
  ]
}
```

---

## Bounding Box Coordinates

The bounding box follows the YOLO/OpenCV coordinate format:

```text
x1 = left
y1 = top
x2 = right
y2 = bottom
```

Example:

```text
[x1, y1, x2, y2]
```

These coordinates can be used by another application to draw bounding boxes around detected objects.

---

## Processed Image Endpoint

The API also provides an endpoint that returns the processed image with YOLO bounding boxes.

```http
POST /predict/image
```

The endpoint:

1. Accepts an image.
2. Runs YOLO inference.
3. Draws bounding boxes around detected objects.
4. Adds class names and confidence scores.
5. Returns the processed image.

This is useful when a frontend application needs to display the visual detection result instead of only receiving JSON data.

---

## Error Handling

The API includes validation and proper HTTP error responses.

Examples of handled errors include:

### Invalid Image

If the uploaded file is not a valid image, the API returns an appropriate HTTP error instead of attempting inference.

Example:

```json
{
  "detail": "Invalid image file"
}
```

### Missing File

If no image is provided:

```json
{
  "detail": "Image file is required"
}
```

### Invalid Confidence Threshold

If an invalid confidence value is provided, the API returns a validation error.

### Internal Processing Error

Unexpected errors during image processing or model inference are handled and returned as HTTP errors rather than crashing the API.

---

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

* View available endpoints
* Upload test images
* Set the confidence threshold
* Execute API requests
* View JSON responses
* Test the processed-image endpoint

---

## Project Structure

```text
Custom-YOLO-Prediction-API/
│
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── predict.py
│   │
│   ├── services/
│   │   └── detector.py
│   │
│   └── schemas/
│       └── response.py
│
├── models/
│   └── best.pt
│
├── output
├── yolo_API_practice.py
│
├── requirements.txt
└── README.md
```

---

## Running the API

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Conclusion

This project demonstrates how a custom-trained YOLO object detection model can be converted into a practical **REST API using FastAPI**.

FastAPI provides the backend interface for receiving images, validating requests, running YOLO inference, and returning structured prediction results. The API can be integrated with web applications, mobile applications, dashboards, or other services that require object detection capabilities.

The project also demonstrates important backend concepts such as API endpoints, file uploads, request validation, JSON responses, confidence thresholds, error handling, and automatic API documentation.

This provides a foundation for deploying computer vision models as reusable and accessible AI services.

---

## Author

**Muhammad Ashhad**


