from flask import Flask, jsonify
import threading
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import os
import sys
# Load your modelpi
model = load_model("code\sign_language_model.h5")

# Set up MediaPipe for hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Init Flask
app = Flask(__name__)
current_gesture = "None"

# Video stream
cap = cv2.VideoCapture(0)

def preprocess_hand(img):
    img = cv2.resize(img, (28, 28))
    img = np.expand_dims(img, axis=(0, -1))  # (1, 28, 28, 1)
    img = img.astype("float32") / 255.0
    return img

def predict_gesture(hand_img):
    processed = preprocess_hand(hand_img)
    prediction = model.predict(processed)
    class_index = np.argmax(prediction)
    return chr(class_index + 65)  # A-Z (adjust as needed)

# Background camera loop
def camera_loop():
    global current_gesture
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get bounding box
                x_vals = [int(lm.x * frame.shape[1]) for lm in hand_landmarks.landmark]
                y_vals = [int(lm.y * frame.shape[0]) for lm in hand_landmarks.landmark]
                x_min, x_max = max(min(x_vals) - 20, 0), min(max(x_vals) + 20, frame.shape[1])
                y_min, y_max = max(min(y_vals) - 20, 0), min(max(y_vals) + 20, frame.shape[0])
                hand_img = frame[y_min:y_max, x_min:x_max]

                if hand_img.size != 0:
                    gray = cv2.cvtColor(hand_img, cv2.COLOR_BGR2GRAY)
                    current_gesture = predict_gesture(gray)
        else:
            current_gesture = "None"

# Flask endpoint
@app.route('/gesture', methods=['GET'])
def get_gesture():
    return jsonify({'gesture': current_gesture})

# Start the camera thread
threading.Thread(target=camera_loop, daemon=True).start()

# Run Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
