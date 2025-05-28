import easyocr
import cv2
import sys
import os
from time import time

class OCRProcessor:
    def __init__(self):
        """Initialize the OCR reader with optimized settings"""
        self.reader = easyocr.Reader(
            lang_list=['en', 'hi'],
            gpu=False,
            quantize=True,
            model_storage_directory=os.path.join('model2', 'model_cache'),
            download_enabled=True,
            detector=True,
            recognizer=True,
            verbose=False
        )
    
    def preprocess_image(self, img_path, target_width=1280):
        """Optimized image loading with smart resizing"""
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Could not read image at {img_path}")
        
        # Calculate resize ratio maintaining aspect ratio
        h, w = img.shape[:2]
        if w > target_width:
            ratio = target_width / w
            img = cv2.resize(img, (target_width, int(h * ratio)))
        
        # Convert to grayscale if color isn't needed
        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img
    
    def perform_ocr(self, image_path):
        """Ultra-optimized OCR pipeline"""
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            
            # Run detection with current version's API
            results = self.reader.readtext(
                img,
                decoder='beamsearch',
                beamWidth=3,
                batch_size=4,
                paragraph=False,
                detail=1
            )
            
            # Extract text (compatible with current EasyOCR version)
            return " ".join([result[1] for result in results])
            
        except Exception as e:
            print(f"OCR ERROR: {str(e)}", file=sys.stderr)
            return ""

# The following function is what will be imported by the main application
def perform_ocr(image_path):
    """
    Standalone function that matches the expected interface
    This creates an OCRProcessor instance and performs OCR
    """
    ocr = OCRProcessor()
    return ocr.perform_ocr(image_path)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ocr.py <image_path>")
        sys.exit(1)
    
    result = perform_ocr(sys.argv[1])
    print(result)