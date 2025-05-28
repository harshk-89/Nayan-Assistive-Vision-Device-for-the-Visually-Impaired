# import face_recognition
# import cv2
# import os
# import glob
# import numpy as np
# from typing import List

# class FaceRecognizer:
#     def __init__(self):
#         """Initialize once during application startup"""
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.frame_resizing = 0.25
#         self._load_known_faces()  # Load faces once during initialization

#     def _load_known_faces(self):
#         """Load known faces from directory (runs once)"""
#         encodings_path = os.path.join(os.path.dirname(__file__), 'images')
#         if os.path.exists(encodings_path):
#             images_path = glob.glob(os.path.join(encodings_path, "*.*"))
            
#             for img_path in images_path:
#                 img = cv2.imread(img_path)
#                 if img is None:
#                     continue

#                 rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#                 basename = os.path.basename(img_path)
#                 filename = os.path.splitext(basename)[0]

#                 encodings = face_recognition.face_encodings(rgb_img)
#                 if encodings:
#                     self.known_face_encodings.append(encodings[0])
#                     self.known_face_names.append(filename)
#             print(f"Loaded {len(self.known_face_names)} known faces")

#     def recognize_faces(self, image_path: str) -> List[str]:
#         """Recognize faces using pre-loaded encodings"""
#         frame = cv2.imread(image_path)
#         if frame is None:
#             return []

#         small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
#         rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

#         recognized_names = []
#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#             name = "Unknown person"

#             face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)
#             if matches[best_match_index]:
#                 name = self.known_face_names[best_match_index]
            
#             recognized_names.append(name)

#         return recognized_names

# # Initialize once when module loads
# recognizer = FaceRecognizer()

# # Interface function (reuses the same recognizer)
# def recognize_faces(image_path: str) -> List[str]:
#     """Main interface function with single recognizer instance"""
#     return recognizer.recognize_faces(image_path)

# # Compatibility alias
# def recognize_objects(image_path: str) -> List[str]:
#     return recognize_faces(image_path)

import face_recognition
import cv2
import os
import glob
import numpy as np
from typing import List, Tuple

class FaceRecognizer:
    def __init__(self):
        """Initialize once during application startup"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25
        self.confidence_threshold = 0.6  # Below this: confident match
        self.unsure_threshold = 0.8     # Between confidence and unsure: possible match
        
        self._load_known_faces()

    def _load_known_faces(self):
        """Load known faces from directory (runs once)"""
        encodings_path = os.path.join(os.path.dirname(__file__), 'images')
        if os.path.exists(encodings_path):
            images_path = glob.glob(os.path.join(encodings_path, "*.*"))
            
            for img_path in images_path:
                img = cv2.imread(img_path)
                if img is None:
                    continue

                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                basename = os.path.basename(img_path)
                filename = os.path.splitext(basename)[0]

                encodings = face_recognition.face_encodings(rgb_img)
                if encodings:
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append(filename)
            print(f"Loaded {len(self.known_face_names)} known faces")

    def _get_face_confidence(self, face_distance: float) -> Tuple[str, str]:
        """Determine confidence level and appropriate message"""
        if face_distance < self.confidence_threshold:
            return ("confident", "")
        elif face_distance < self.unsure_threshold:
            return ("unsure", "I'm not sure, but this might be ")
        return ("unknown", "Unknown person")

    def recognize_faces(self, image_path: str) -> List[str]:
        """Recognize faces with confidence analysis"""
        frame = cv2.imread(image_path)
        if frame is None:
            return []

        # Preprocess frame
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect all faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        recognized_faces = []
        if not self.known_face_encodings:
            return ["Unknown person"] * len(face_encodings)

        for face_encoding in face_encodings:
            # Calculate distances to known faces
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            min_distance = face_distances[best_match_index]

            # Determine confidence level
            confidence, prefix = self._get_face_confidence(min_distance)
            name = self.known_face_names[best_match_index] if confidence != "unknown" else ""

            # Format response based on confidence
            if confidence == "confident":
                recognized_faces.append(name)
            elif confidence == "unsure":
                recognized_faces.append(f"{prefix}{name}")
            else:
                recognized_faces.append(prefix)

        return recognized_faces

# Initialize once when module loads
recognizer = FaceRecognizer()

def recognize_faces(image_path: str) -> List[str]:
    """Main interface function"""
    return recognizer.recognize_faces(image_path)

def recognize_objects(image_path: str) -> List[str]:
    return recognize_faces(image_path)

if __name__ == "__main__":
    test_img = "test.jpg"
    if os.path.exists(test_img):
        results = recognize_faces(test_img)
        print("Recognized faces:", ", ".join(results))
    else:
        print(f"Test image {test_img} not found")