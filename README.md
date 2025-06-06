# Nayan – Assistive Vision Device for the Visually Impaired

**Nayan** is an offline, AI-powered assistive vision system designed to help visually impaired users navigate their environment. By combining voice feedback, object detection, face recognition, and image-to-text capabilities, Nayan provides real-time audio descriptions without requiring an internet connection.

---

## 🔧 Modules

- **Voice Module (`pyttsx3`)**  
  Converts text into speech so that all detected information can be communicated audibly to the user.

- **Image-to-Text Module (`EasyOCR`)**  
  Extracts text from images (e.g., signs, documents) and passes it to the Voice Module for audio playback.

- **Face Detection & Recognition Module (`face_recognition`, `dlib`, `opencv-python`)**  
  Detects faces in the camera feed, compares them against a known-face database, and announces recognized names (or indicates “Unknown Face”).

- **Object Detection Module (`YOLOv8` via `ultralytics`)**  
  Performs real-time object detection, annotates each detected object with a bounding box and label, and provides spoken descriptions or distance estimates (e.g., “chair detected,” “person far away”).

---

## 🛠️ Installation

1. **fork & Clone the repository**  
   Replace `YOUR-GITHUB-USERNAME` with your GitHub username:
   ```bash
   git clone https://github.com/YOUR-GITHUB-USERNAME/Nayan-Assistive-Vision-Device-for-the-Visually-Impaired.git
   cd Nayan-Assistive-Vision-Device-for-the-Visually-Impaired

2. **Create and activate a virtual environment**

   ```bash
   python3.10 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **(Optional) If `dlib` fails to build from source**
   Install the provided precompiled wheel:

   ```bash
   pip install dlib-19.24.0-cp310-cp310-win_amd64.whl
   ```

---

## 🚀 Usage

1. **Prepare your known faces folder**

   * Add clear, frontal images of people you want the system to recognize.
   * Ensure each image filename reflects the person’s name (e.g., `alice.jpg`, `bob.png`).

2. **Adjust configuration (if needed)**

   * In `config.py` (or whichever config file), set any paths or thresholds:

     * Path to known-face directory
     * Confidence thresholds for face recognition
     * YOLOv8 model path (e.g., `yolov8m.pt`)
     * OCR language preferences

3. **Run the main application**

   ```bash
   python main.py
   ```

   * The system will initialize all modules in sequence.
   * You will hear spoken prompts and continuous audio descriptions as the camera feed is processed.

4. **Stopping the application**

   * Press `Ctrl+C` (or close the terminal) to stop the program and release the camera device.

---

## 🤝 Contributing

We welcome contributions! To help improve Nayan:

1. **Fork** this repository.
2. **Clone** your fork:

   ```bash
   git clone https://github.com/YOUR-GITHUB-USERNAME/Nayan-Assistive-Vision-Device-for-the-Visually-Impaired.git
   ```
3. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes, commit, and push:

   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin feature/your-feature-name
   ```
5. Open a **Pull Request** on the main repository. We’ll review and merge if everything looks good!

