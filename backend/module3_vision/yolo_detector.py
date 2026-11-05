from ultralytics import YOLO
import os

# Initialize YOLOv8 model placeholder (e.g., using yolov8n.pt or a custom-trained model)
# It will auto-download 'yolov8n.pt' if a custom weights path doesn't exist
model = None

def load_yolo_model(weights_path='yolov8n.pt'):
    """Loads the YOLOv8 model from the given path."""
    global model
    if model is None:
        model = YOLO(weights_path)
        print(f"YOLO model loaded using weights: {weights_path}")
    return model

def detect_objects(image_path, weights_path='yolov8n.pt'):
    """Runs YOLOv8 object detection on an image and returns structured detections."""
    try:
        yolo_model = load_yolo_model(weights_path)
        
        # Run inference
        results = yolo_model(image_path, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Extract box coordinates (x_min, y_min, x_max, y_max)
                xyxy = box.xyxy[0].tolist()
                x_min, y_min, x_max, y_max = xyxy
                
                # Get class label
                class_idx = int(box.cls[0].item())
                label = yolo_model.names[class_idx]
                
                # Get confidence
                confidence = float(box.conf[0].item())
                
                detections.append({
                    'label': label,
                    'box': [round(x_min, 2), round(y_min, 2), round(x_max, 2), round(y_max, 2)],
                    'confidence': round(confidence, 4)
                })
        
        return detections
    except Exception as e:
        return {
            'error': str(e)
        }
