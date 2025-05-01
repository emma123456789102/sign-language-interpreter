import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from flask import Flask, jsonify
import threading
import time
import os

# === Load Model ===
model_path = "C:/Users/Emma Davidson/PycharmProjects/sign-language-interpreter/code/sign_language_model.h5"

if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

try:
    model = load_model(model_path)
    print("✅ Model loaded successfully!")
except Exception as e:
    print("❌ Failed to load model:", e)

# === MediaPipe Setup ===
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.85)

# === Video Capture Setup ===
video_stream = cv2.VideoCapture(0)
if not video_stream.isOpened():
    print("❌ Webcam not accessible.")
    exit()

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
desired_fps = 30
frame_time = 1 / desired_fps

# === Flask Setup ===
app = Flask(__name__)
current_gesture = "None"
gesture_history = []
min_consecutive = 6


def preprocess_hand_roi(img):
    """Resize and normalize hand ROI for model."""
    img = cv2.resize(img, (28, 28))
    img = img.astype('float32') / 255.0
    img = np.reshape(img, (1, 28, 28, 1))
    return img


def predict_gesture(roi_gray):
    """Run model prediction."""
    processed = preprocess_hand_roi(roi_gray)
    prediction = model.predict(processed, verbose=0)
    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction)
    return chr(predicted_class + 65), confidence


@app.route('/gesture', methods=['GET'])
def get_gesture():
    return jsonify({'gesture': current_gesture})


def capture_loop():
    global current_gesture, gesture_history
    while True:
        start_time = time.time()
        ret, frame = video_stream.read()
        if not ret:
            break

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                x_vals = [lm.x for lm in hand_landmarks.landmark]
                y_vals = [lm.y for lm in hand_landmarks.landmark]
                x_min = int(min(x_vals) * FRAME_WIDTH)
                y_min = int(min(y_vals) * FRAME_HEIGHT)
                x_max = int(max(x_vals) * FRAME_WIDTH)
                y_max = int(max(y_vals) * FRAME_HEIGHT)

                # Make box square and centered
                box_size = max(x_max - x_min, y_max - y_min) + 40
                center_x = (x_min + x_max) // 2
                center_y = (y_min + y_max) // 2
                x_min = max(center_x - box_size // 2, 0)
                y_min = max(center_y - box_size // 2, 0)
                x_max = min(center_x + box_size // 2, FRAME_WIDTH)
                y_max = min(center_y + box_size // 2, FRAME_HEIGHT)

                hand_roi = frame[y_min:y_max, x_min:x_max]
                if hand_roi.shape[0] > 0 and hand_roi.shape[1] > 0:
                    gray_hand = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
                    cv2.imshow("Hand ROI", gray_hand)  # Debug view

                    letter, confidence = predict_gesture(gray_hand)
                    print(f" Predicted: {letter} | Confidence: {confidence:.2f}")

                    if confidence >= 0.8:
                        gesture_history.append(letter)
                        if len(gesture_history) > min_consecutive:
                            gesture_history.pop(0)

                        # Consistency check
                        if len(gesture_history) == min_consecutive:
                            most_common = max(set(gesture_history), key=gesture_history.count)
                            if gesture_history.count(most_common) >= 5:
                                current_gesture = most_common
                                cv2.putText(frame, current_gesture, (x_min, y_min - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                    else:
                        gesture_history = []

        cv2.imshow("Live Feed - ASL Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

        time.sleep(max(0, frame_time - (time.time() - start_time)))

    video_stream.release()
    cv2.destroyAllWindows()


# === Run threads ===
threading.Thread(target=capture_loop, daemon=True).start()
app.run(port=5000)
#hello