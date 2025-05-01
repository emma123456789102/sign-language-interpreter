from flask import Flask, jsonify
import threading
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from flask_cors import CORS
from deepface import DeepFace
import time

# Load the gesture recognition model
model = load_model("code/sign_language_model.h5")

# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Setup Flask app
app = Flask(__name__)
CORS(app)

# Global state
current_gesture = "None"
current_emotion = "N/A"
cap = cv2.VideoCapture(0)

def preprocess_hand(img):
    img = cv2.resize(img, (28, 28))
    img = np.expand_dims(img, axis=(0, -1))  # Shape: (1, 28, 28, 1)
    img = img.astype("float32") / 255.0
    return img

def predict_gesture(hand_img):
    processed = preprocess_hand(hand_img)
    prediction = model.predict(processed, verbose=0)
    class_index = np.argmax(prediction)
    return chr(class_index + 65)  # A-Z

def analyze_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "N/A"

def camera_loop():
    global current_gesture, current_emotion

    frame_count = 0  # For reducing DeepFace frequency

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # --- Hand detection & prediction ---
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x_vals = [int(lm.x * frame.shape[1]) for lm in hand_landmarks.landmark]
                y_vals = [int(lm.y * frame.shape[0]) for lm in hand_landmarks.landmark]
                x_min, x_max = max(min(x_vals) - 20, 0), min(max(x_vals) + 20, frame.shape[1])
                y_min, y_max = max(min(y_vals) - 20, 0), min(max(y_vals) + 20, frame.shape[0])
                hand_img = frame[y_min:y_max, x_min:x_max]

                if hand_img.size != 0:
                    gray = cv2.cvtColor(hand_img, cv2.COLOR_BGR2GRAY)
                    current_gesture = predict_gesture(gray)

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            current_gesture = "None"

        # --- Emotion analysis every few frames to reduce lag ---
        if frame_count % 30 == 0:
            current_emotion = analyze_emotion(frame)
        frame_count += 1

        # Display info on frame
        cv2.putText(frame, f"Gesture: {current_gesture}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        cv2.putText(frame, f"Emotion: {current_emotion}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 100, 100), 2)

        cv2.imshow("Sign + Emotion Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# API routes
@app.route('/gesture', methods=['GET'])
def get_gesture():
    return jsonify({'gesture': current_gesture})

@app.route('/emotion', methods=['GET'])
def get_emotion():
    return jsonify({'emotion': current_emotion})

if __name__ == "__main__":
    threading.Thread(target=camera_loop, daemon=True).start()
    time.sleep(1)
    app.run(host="0.0.0.0", port=5000)