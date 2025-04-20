# sign-language-interpreter

📁 BSL-Interpreter-AR
│── 📂 data            # BSL dataset & extracted keypoints
│── 📂 models          # Trained machine learning models
│── 📂 scripts         # Python & R scripts for processing
│── 📂 ar_display      # AR overlay for captions (Unity/OpenCV)
│── README.md         # Project documentation
🛠️ Installation
1️⃣ Install Dependencies
Make sure you have **Python 3.7 - 3.10** installed. 


### 2️⃣ Setup Virtual Environments
The hand tracking and RASA have incompatible package requirements, so two virtual environments should be configured

# Terminal 1 (Hand Tracking)
```bash
python -m venv venv_tracking
source venv_tracking/bin/activate  # Mac/Linux
venv_tracking\Scripts\activate     # Windows
pip install mediapipe opencv-python numpy pandas tensorflow keras flask
```
If using R for training:

install.packages("randomForest")
install.packages("keras")

# Terminal 2 (RASA)
```bash
py -3.10 -m venv venv_rasa
source venv_rasa/bin/activate  # Mac/Linux
venv_rasa\Scripts\activate     # Windows
pip install rasa
```

git clone https://github.com/your-repo/BSL-Interpreter-AR.git
cd BSL-Interpreter-AR
🎥 How It Works
Step 1: Capture Video Input
The AR glasses camera records the signer’s gestures in real-time.

import cv2
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("BSL Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break
cap.release()
cv2.destroyAllWindows()
Step 2: Extract Hand & Pose Keypoints
Using Mediapipe, we track hand and body movement.

import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
Step 3: Train AI Model (Using R or Python)
Train a Random Forest Model in R
library(randomForest)
data <- read.csv("bsl_dataset.csv")
model <- randomForest(label ~ ., data=data, ntree=200)
saveRDS(model, "bsl_rf_model.rds")
Train a Deep Learning Model in Python
from tensorflow.keras.models import Sequential
model = Sequential([...])
model.fit(X_train, y_train, epochs=50, batch_size=16)
model.save("bsl_model.h5")
Step 4: Real-Time Captioning in AR
Overlay text captions on AR glasses using OpenCV or Unity.

cv2.putText(frame, "Hello!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

### 4️⃣ Run Virtual Environments
Open three terminal windows. Run the tracking venv in terminal 1, then the rasa venv in terminals 2 and 3.

Terminal 1: python code/hand_tracking.py
Terminal 2: rasa run actions
Terminal 3: rasa shell 

If changing intents, retrain the model with 'rasa train' in a rasa venv.

# RASA shell
'What gesture is this?'
'Test me'

📌 Challenges & Future Improvements
❌ Improve BSL recognition accuracy with a larger dataset ❌ Implement sentence-level sign translation ❌ Optimize for real-time AR processing
 4️⃣ Connecting the glasses

to run the unity, please run the launch.json file which is located within the repostory.
once this is run also run the Flask_app.py once these are both run this should allow you to 
run the programme.

💡 Contributors
**Emma Davidson** - AI/ML Specialist/ Unity Developer /Rasa Developer 
**Annie O'boyle**  - essay writter
**Neil** - Dialogue Management and RASA integration
**Sarah Jade Ruthven**  - Unity Developer


📜 License
This project is licensed under the MIT License.

🌟 Let’s break communication barriers with AI & AR! 🚀
