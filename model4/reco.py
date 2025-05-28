import os
import cv2
from ultralytics import YOLO
from datetime import datetime
from typing import Dict, List

class ObjectRecognizer:
    def __init__(self):
        """Initialize the object recognition system"""
        self.model = YOLO('yolov8l.pt')
        self.conf_threshold = 0.4
        self.close_threshold = 0.2
        self.prev_counts = {}
        
    def recognize_objects(self, image_path: str) -> List[str]:
        """
        Perform object recognition on an image
        :param image_path: Path to the image file
        :return: List of detected objects (formatted strings)
        """
        try:
            # Read and process image
            frame = cv2.imread(image_path)
            if frame is None:
                raise ValueError(f"Could not read image at {image_path}")
            
            h, w = frame.shape[:2]
            
            # Run YOLO inference
            result = self.model(frame)[0]
            boxes = result.boxes
            
            # Process detections
            counts = {}
            for box in boxes:
                conf = float(box.conf[0])
                if conf < self.conf_threshold:
                    continue
                
                cls_id = int(box.cls[0])
                name = self.model.names[cls_id]
                counts[name] = counts.get(name, 0) + 1
            
            # Format results
            objects = []
            for cls, cnt in counts.items():
                label = cls + ("s" if cnt > 1 else "")
                objects.append(f"{cnt} {label}")
            
            self.prev_counts = counts.copy()
            return objects
            
        except Exception as e:
            print(f"Recognition error: {str(e)}")
            return []

    def save_annotated_image(self, image_path: str, output_dir: str = "captures") -> str:
        """
        Save an annotated version of the image with detection results
        :param image_path: Path to the original image
        :param output_dir: Directory to save annotated image
        :return: Path to saved annotated image
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            frame = cv2.imread(image_path)
            if frame is None:
                raise ValueError(f"Could not read image at {image_path}")
            
            h, w = frame.shape[:2]
            result = self.model(frame)[0]
            boxes = result.boxes
            
            # Draw detections
            counts = {}
            for box in boxes:
                conf = float(box.conf[0])
                if conf < self.conf_threshold:
                    continue
                
                cls_id = int(box.cls[0])
                name = self.model.names[cls_id]
                counts[name] = counts.get(name, 0) + 1
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                box_w = x2 - x1
                dist_label = "close" if (box_w / w) > self.close_threshold else "far"
                text = f"{name} ({dist_label})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, text, (x1, y1 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            
            # Add counts overlay
            y0 = 20
            for cls, cnt in counts.items():
                cv2.putText(frame, f"{cls}: {cnt}", (10, y0),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
                y0 += 25
            
            # Save annotated image
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            cnt_str = "_".join(f"{k}{v}" for k,v in counts.items())
            fname = f"{ts}_{cnt_str}.jpg"
            output_path = os.path.join(output_dir, fname)
            cv2.imwrite(output_path, frame)
            
            return output_path
            
        except Exception as e:
            print(f"Error saving annotated image: {str(e)}")
            return ""

# The following function is what will be imported by the main application
def recognize_objects(image_path: str) -> List[str]:
    """
    Standalone function that matches the expected interface
    :param image_path: Path to the image file
    :return: List of detected objects (formatted strings)
    """
    recognizer = ObjectRecognizer()
    return recognizer.recognize_objects(image_path)

# Example usage
if __name__ == "__main__":
    # Test the recognition
    test_image = "test.jpg"
    if os.path.exists(test_image):
        detected_objects = recognize_objects(test_image)
        print("Detected objects:", ", ".join(detected_objects))
        
        # Test saving annotated image
        saved_path = ObjectRecognizer().save_annotated_image(test_image)
        if saved_path:
            print(f"Saved annotated image to: {saved_path}")
    else:
        print(f"Test image {test_image} not found")