# BSL Interpreter for AR Glasses

## 📌 Project Overview
This project aims to develop a **British Sign Language (BSL) Interpreter** that runs on **AR glasses**. The system captures real-time **BSL gestures**, translates them into **text**, and displays captions on **augmented reality (AR) glasses**.

## 🚀 Features
✅ **Real-time BSL recognition** using hand and body tracking
✅ **Machine learning-powered sign language translation**
✅ **Text overlay in AR glasses** for live captions
✅ **Optimized for low-latency performance**

## 📂 Project Structure
```
📁 BSL-Interpreter-AR
│── 📂 data            # BSL dataset & extracted keypoints
│── 📂 models          # Trained machine learning models
│── 📂 scripts         # Python & R scripts for processing
│── 📂 ar_display      # AR overlay for captions (Unity/OpenCV)
│── README.md         # Project documentation
```

## 🛠️ Installation
### 1️⃣ Install Dependencies
Make sure you have **Python 3.7 - 3.10** installed. Then, install required libraries:
```bash
pip install mediapipe opencv-python numpy pandas tensorflow keras
```
If using R for training:
```r
install.packages("randomForest")
install.packages("keras")
```

### 2️⃣ Setup Virtual Environment (Recommended)
```bash
python -m venv bsl_env
source bsl_env/bin/activate  # Mac/Linux
bsl_env\Scripts\activate     # Windows
```

### 3️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/BSL-Interpreter-AR.git
cd BSL-Interpreter-AR
```

## 🎥 How It Works
### Step 1: Capture Video Input
The AR glasses camera records the **signer’s gestures** in real-time.
```python
import cv2
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("BSL Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break
cap.release()
cv2.destroyAllWindows()
```

### Step 2: Extract Hand & Pose Keypoints
Using **Mediapipe**, we track **hand and body movement**.
```python
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
```

### Step 3: Train AI Model (Using R or Python)
#### Train a Random Forest Model in R
```r
library(randomForest)
data <- read.csv("bsl_dataset.csv")
model <- randomForest(label ~ ., data=data, ntree=200)
saveRDS(model, "bsl_rf_model.rds")
```
#### Train a Deep Learning Model in Python
```python
from tensorflow.keras.models import Sequential
model = Sequential([...])
model.fit(X_train, y_train, epochs=50, batch_size=16)
model.save("bsl_model.h5")
```

### Step 4: Real-Time Captioning in AR
Overlay text captions on **AR glasses** using OpenCV or Unity.
```python
cv2.putText(frame, "Hello!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
```

## 📌 Challenges & Future Improvements
❌ Improve **BSL recognition accuracy** with a larger dataset
❌ Implement **sentence-level sign translation**
❌ Optimize for **real-time AR processing**

## 💡 Contributors
- **Emma Davidson** - Developer
- **Jade Ruthven** - ASL Signer & UREAL Developer

## 📜 License
This project is licensed under the **MIT License**.

---
🌟 **Let’s break communication barriers with AI & AR!** 🚀

