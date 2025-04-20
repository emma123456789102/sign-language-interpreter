import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from flask import Flask, jsonify
import threading

import os
from tensorflow.keras.models import load_model

model_path = "sign_language_model.h5"
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

try:
    model = load_model(model_path)
    print("✅ Model loaded successfully!")
except Exception as e:
    print("❌ Error loading model:", e)


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Video capture
video_stream = cv2.VideoCapture(1)

# Frame dimensions
FRAME_WIDTH = 600
FRAME_HEIGHT = 400

def preprocess_hand_roi(img):
    """ Prepares the hand ROI for CNN model prediction. """
    img = cv2.resize(img, (64, 64))  # Resize to match model input
    img = np.expand_dims(img, axis=[0, -1])  # Add batch and channel dimensions
    img = img / 255.0  # Normalize
    return img

def predict_gesture(hand_roi):
    """ Predicts the static gesture using the trained CNN model. """
    processed_img = preprocess_hand_roi(hand_roi)
    prediction = model.predict(processed_img)
    predicted_class = np.argmax(prediction)
    return chr(predicted_class + 65)  # Convert to letter (A-Z)

current_gesture = None
test_gesture = None
confidence_count = 0

def get_current_gesture():
    global current_gesture
    return current_gesture

app = Flask(__name__)

def capture_loop():
    global current_gesture, test_gesture, confidence_count
    while True:
        ret, frame = video_stream.read()
        if not ret:
            break  # Exit if camera feed is lost

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame = cv2.flip(frame, 1)  # Mirror for intuitive interaction
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the hand
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get bounding box around the hand
                x_min, y_min = float("inf"), float("inf")
                x_max, y_max = float("-inf"), float("-inf")

                for landmark in hand_landmarks.landmark:
                    x, y = int(landmark.x * FRAME_WIDTH), int(landmark.y * FRAME_HEIGHT)
                    x_min, y_min = min(x_min, x), min(y_min, y)
                    x_max, y_max = max(x_max, x), max(y_max, y)

                # Expand bounding box slightly
                x_min, y_min = max(0, x_min - 20), max(0, y_min - 20)
                x_max, y_max = min(FRAME_WIDTH, x_max + 20), min(FRAME_HEIGHT, y_max + 20)

                # Extract hand region
                hand_roi = frame[y_min:y_max, x_min:x_max]
                if hand_roi.shape[0] > 0 and hand_roi.shape[1] > 0:
                    gray_hand = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
                    letter = predict_gesture(gray_hand)

                    if letter == test_gesture:
                        confidence_count += 1
                    else:
                        test_gesture = letter
                        confidence_count = 0

                    if confidence_count > 5:   # Only update if gesture remains constant for 5 frames
                        current_gesture = letter
                        confidence_count = 0

                    # Display prediction
                    cv2.putText(frame, letter, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show frame
        cv2.imshow("Live Feed - Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    # Cleanupsa
    video_stream.release()
    cv2.destroyAllWindows()

# API endpoints
@app.route('/gesture', methods=['GET'])
def get_gesture():
    return jsonify({'gesture': current_gesture})

@app.route('/gesture/reset', methods=['POST'])
def reset_gesture():
    global current_gesture
    current_gesture = None
    print("[Tracking] Gesture reset.")
    return jsonify({'status': 'ok', 'gesture': current_gesture})

threading.Thread(target=capture_loop, daemon=True).start()

app.run(port=5000)
