import cv2
import sys
import os
import time

# Configuration
CAPTURE_DIR = "captures"
os.makedirs(CAPTURE_DIR, exist_ok=True)
PROCESS_INTERVAL = 2  # seconds between processing

def load_models():
    """Dynamically import model functions"""
    try:
        from model1.voice import text_to_speech
        from model2.ocr import perform_ocr
        from model3.face_detection import recognize_faces
        from model4.reco import recognize_objects
        return {
            'tts': text_to_speech,
            'ocr': perform_ocr,
            'face': recognize_faces,
            'reco': recognize_objects
        }
    except ImportError as e:
        print(f"Error loading models: {str(e)}")
        sys.exit(1)

def main():
    models = load_models()
    mode = 1  # 1: YOLO, 2: face Recognition, 3: OCR
    last_processed = 0
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Blind Assistance System Ready")
    print("Press 1: Captioning, 2: Recognition, 3: OCR, q: Quit")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            current_time = time.time()
            
            # Process frame if interval has elapsed
            if current_time - last_processed >= PROCESS_INTERVAL:
                timestamp = int(time.time())
                img_path = os.path.join(CAPTURE_DIR, f"frame_{timestamp}.jpg")
                cv2.imwrite(img_path, frame)
                
                try:
                    if mode == 1:
                        objects = models['reco'](img_path)
                        if objects:  # Only speak if objects detected
                            models['tts'](f"I see {', '.join(objects)}")
                    elif mode == 2:
                        caption = models['face'](img_path)
                        if caption:
                            models['tts'](f"I think this is {caption}")
                    elif mode == 3:
                        text = models['ocr'](img_path)
                        models['tts'](f"I read: {text}" if text else "No text detected")
                    
                    last_processed = current_time
                    os.remove(img_path)
                except Exception as e:
                    print(f"Processing error: {str(e)}")
            
            # Non-GUI key detection
            if sys.platform == 'win32':
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode()
                    if key == 'q':
                        break
                    elif key in ('1', '2', '3'):
                        mode = int(key)
                        mode_names = {1: "Captioning", 2: "Recognition", 3: "OCR"}
                        models['tts'](f"{mode_names.get(mode, '')} mode activated")
            else:
                # Linux/Mac alternative would go here
                pass
    
    finally:
        cap.release()

if __name__ == "__main__":
    main()


# import cv2
# import sys
# import os
# import time

# # Configuration
# CAPTURE_DIR = "captures"
# os.makedirs(CAPTURE_DIR, exist_ok=True)
# PROCESS_INTERVAL = 2  # seconds between processing

# def load_models():
#     """Dynamically import model functions"""
#     try:
#         from model1.voice import text_to_speech
#         from model2.ocr import perform_ocr
#         from model3.face_detection import recognize_faces
#         from model4.reco import recognize_objects
#         return {
#             'tts': text_to_speech,
#             'ocr': perform_ocr,
#             'face': recognize_faces,
#             'reco': recognize_objects
#         }
#     except ImportError as e:
#         print(f"Error loading models: {str(e)}")
#         sys.exit(1)

# def main():
#     models = load_models()
#     mode = 1  # 1: YOLO, 2: face Recognition, 3: OCR
#     last_processed = 0
    
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open camera")
#         return
    
#     print("Blind Assistance System Ready")
#     print("Press 1: Captioning, 2: Recognition, 3: OCR, q: Quit")
    
#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("Error: Could not read frame")
#                 break
            
#             current_time = time.time()
            
#             # Process frame if interval has elapsed
#             if current_time - last_processed >= PROCESS_INTERVAL:
#                 timestamp = int(time.time())
#                 img_path = os.path.join(CAPTURE_DIR, f"frame_{timestamp}.jpg")
#                 cv2.imwrite(img_path, frame)
                
#                 try:
#                     if mode == 1:
#                         objects = models['reco'](img_path)
#                         if objects:  # Only speak if objects detected
#                             models['tts'](f"I see {', '.join(objects)}")
#                     # In main.py's processing block (mode == 2 case):
#                     elif mode == 2:
#                         captions = models['face'](img_path)
#                         if captions:
#                             # Join multiple results with natural language
#                             if len(captions) == 1:
#                                 print(captions[0])
#                                 models['tts'](f"I see {captions[0]}")
#                             else:
#                                 last = captions.pop()
#                                 print(last)
#                                 models['tts'](f"I see {', '.join(captions)}, and {last}")
#                         # else:
#                         #     models['tts']("No faces detected")
#                     elif mode == 3:
#                         text = models['ocr'](img_path)
#                         models['tts'](f"I read: {text}" if text else "No text detected")
                    
#                     last_processed = current_time
#                     os.remove(img_path)
#                 except Exception as e:
#                     print(f"Processing error: {str(e)}")
            
#             # Non-GUI key detection
#             if sys.platform == 'win32':
#                 import msvcrt
#                 if msvcrt.kbhit():
#                     key = msvcrt.getch().decode()
#                     if key == 'q':
#                         break
#                     elif key in ('1', '2', '3'):
#                         mode = int(key)
#                         mode_names = {1: "Captioning", 2: "Recognition", 3: "OCR"}
#                         models['tts'](f"{mode_names.get(mode, '')} mode activated")
#             else:
#                 # Linux/Mac alternative would go here
#                 pass
    
#     finally:
#         cap.release()

# if __name__ == "__main__":
#     main()