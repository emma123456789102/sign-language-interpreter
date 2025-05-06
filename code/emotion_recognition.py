from flask import Flask, jsonify, request
from deepface import DeepFace
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/analyze-emotion', methods=['POST'])
def analyze_emotion():
    try:
        file = request.files['frame']
        npimg = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return jsonify({'emotion': result[0]['dominant_emotion']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(port=5050)
