# 🧠 Sign Language Interpreter – ASL Interpreter for AR Glasses

A multi-component system that uses machine learning, computer vision, a webcam, and natural language processing to interpret American Sign Language (ASL) in real time.

---

## 📁 Project Structure

sign-language-interpreter/
├── data/ # ASL dataset & extracted keypoints
├── models/ # Trained machine learning models
├── actions/ # RASA action components
├── code/ # Python & R scripts for processing
├── ar_display/ # AR overlay for captions (Unity/OpenCV)
├── tests/ # Python model testing for essay
├── app/ # flask_app.py
├── config.yml
├── credentials.yml
├── domain.yml
├── endpoints.yml
├── sign_language_model.h5
├── training_history.png
└── README.md # Project documentation

yaml


---

## 🛠️ Installation

### 1️⃣ Install Dependencies

Ensure you have **Python 3.7–3.10** installed.

### 2️⃣ Set Up Virtual Environments

Due to incompatible package requirements between the hand tracking module and RASA, two virtual environments are needed.

---

#### Terminal 1 – Hand Tracking

```bash
python -m venv venv_tracking
source venv_tracking/bin/activate        # Mac/Linux
venv_tracking\Scripts\activate           # Windows
pip install mediapipe opencv-python numpy pandas tensorflow keras flask flask-cors deepface tf-keras
Optional R packages for training in R:

r

install.packages("randomForest")
install.packages("keras")
Terminal 2 – RASA
bash

#### Terminal 2 – RASA
py -3.10 -m venv venv_rasa
source venv_rasa/bin/activate            # Mac/Linux
venv_rasa\Scripts\activate               # Windows
pip install rasa pyttsx3 SpeechRecognition pyaudio
🎥 How It Works
📷 Step 1: Capture Video Input
python

import cv2

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("ASL Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
✋ Step 2: Extract Hand & Pose Keypoints (Mediapipe)
python

import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
🧠 Step 3: Train AI Model
In R:
r

library(randomForest)
data <- read.csv("asl_dataset.csv")
model <- randomForest(label ~ ., data = data, ntree = 200)
saveRDS(model, "asl_rf_model.rds")
In Python:
python

from tensorflow.keras.models import Sequential

model = Sequential([...])
model.fit(X_train, y_train, epochs=50, batch_size=16)
model.save("asl_model.h5")
🔄 Quick Demo
Run everything with:

''bash

python run_all.py
This sets up and launches all required services using the correct virtual environments.

🐞 Debug Mode (4-Terminal Setup)
Open four terminals:

Terminal 1: Hand tracking

bash

python code/hand_tracking.py
Terminal 2: RASA actions

bash

rasa run actions
Terminal 3: RASA server

bash

rasa run --enable-api --cors "*" --debug
Terminal 4: Speech handler

bash

python handlers/speech_handler.py
To retrain intents, run:

bash

rasa train
Try sample prompts:

kotlin

> What gesture is this?
> Test me

---
📌 Challenges & Future Improvements
❌ Improve ASL recognition accuracy with a larger dataset

❌ Implement sentence-level sign translation

❌ Optimize real-time AR performance for mobile/edge devices

## 💡 Contributors

| Name                | Role(s)                                                         |
|---------------------|------------------------------------------------------------------|
| **Emma Davidson**   | AI/ML Specialist • Unity Developer • RASA Developer             |
| **Annie O'Boyle**   | Essay Writer • Documentation                                     |
| **Neil**            | Dialogue Management • RASA Integration                          |
| **Sarah Jade Ruthven** | Unity Developer • Facial Recognition • Sign Animation      |

📜 License
This project is licensed under the MIT License.

🌟 Final Thoughts
Let’s break communication barriers with the power of AI and AR.
Real-time. Accessible. Inclusive.

yaml
Copy


---









