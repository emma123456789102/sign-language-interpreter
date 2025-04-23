🧠 Sign Language Interpreter – ASL Interpreter for AR Glasses
A multi-component system that uses machine learning, computer vision, AR glasses, and natural language processing to interpret British Sign Language (BSL) in real time.

📁 Project Structure
bash
Copy
Edit
📂 BSL-Interpreter-AR
├── 📂 data          # ASL dataset & extracted keypoints
├── 📂 models        # Trained machine learning models
├── 📂 actions       # rasa run components
├── 📂 code      # Python & R scripts for processing
├── 📂 ar_display    # AR overlay for captions (Unity/OpenCV)
├── 📂 tests         #testing the pythin model for essay
├── 📂 app              # flask_app.py
├──config.yml
├──credentials.yml
├── domain.yml
├──endpoints.yml
├──sign_language_model.h5
├──training_history.png
├── README.md        # Project documentation

🛠️ Installation
1️⃣ Install Dependencies
Ensure you have Python 3.7–3.10 installed.

2️⃣ Setup Virtual Environments
Hand tracking and RASA have incompatible dependencies, so two virtual environments are required.

Terminal 1: Hand Tracking (Python)
bash
Copy
Edit
python -m venv venv_tracking
source venv_tracking/bin/activate     # Mac/Linux
venv_tracking\Scripts\activate        # Windows

pip install mediapipe opencv-python numpy pandas tensorflow keras flask
If using R for training:
R
Copy
Edit
install.packages("randomForest")
install.packages("keras")
Terminal 2: RASA
bash
Copy
Edit
python -m venv venv_rasa
source venv_rasa/bin/activate         # Mac/Linux
venv_rasa\Scripts\activate            # Windows

pip install rasa
🎥 How It Works
📷 Step 1: Capture Video Input
Use OpenCV to access the webcam:

python
Copy
Edit
import cv2

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("BSL Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
✋ Step 2: Extract Hand & Pose Keypoints (Mediapipe)
python
Copy
Edit
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
🧠 Step 3: Train AI Model
In R:
R
Copy
Edit
library(randomForest)
data <- read.csv("bsl_dataset.csv")
model <- randomForest(label ~ ., data = data, ntree = 200)
saveRDS(model, "bsl_rf_model.rds")
In Python:
python
Copy
Edit
from tensorflow.keras.models import Sequential

model = Sequential([...])
model.fit(X_train, y_train, epochs=50, batch_size=16)
model.save("bsl_model.h5")
🕶️ Step 4: Real-Time Captioning in AR
Overlay predictions using OpenCV or Unity:

python
Copy
Edit
cv2.putText(frame, "Hello!", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
🧪 Running the Project
Open three terminal windows:

Terminal 1: Activate tracking venv and run hand tracking:

bash
Copy
Edit
source venv_tracking/bin/activate
python scripts/hand_tracking.py
Terminal 2: Activate RASA venv and run actions:

bash
Copy
Edit
source venv_rasa/bin/activate
rasa run actions
Terminal 3: Run RASA shell:

bash
Copy
Edit
rasa shell
To update RASA intents, run:

bash
Copy
Edit
rasa train
🕶️ Connecting to the AR Glasses (Unity)
To run the Unity integration:

Open the project in Unity.

Make sure launch.json is set up (for debugging).

Start flask_app.py in the tracking virtual environment:

bash
Copy
Edit
python flask_app.py
Press Play in Unity. Gesture data should now stream from Flask to Unity and display in the AR overlay.

📌 Challenges & Future Improvements
❌ Improve ASL recognition accuracy with a larger dataset

❌ Implement sentence-level sign translation

❌ Optimise real-time AR performance for mobile/edge devices

💡 Contributors

Name	Role
Emma Davidson	AI/ML Specialist • Unity Developer • RASA Developer
Annie O'Boyle	Essay Writer & Documentation
Neil	Dialogue Management • RASA Integration
Sarah Jade Ruthven	Unity Developer
📜 License
This project is licensed under the MIT License.

🌟 Final Thoughts
Let’s break communication barriers with the power of AI and AR.
Real-time. Accessible. Inclusive.
