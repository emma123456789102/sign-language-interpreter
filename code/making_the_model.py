import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import confusion_matrix, classification_report

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ---------------------------
# 1. Load Dataset
# ---------------------------
train_df = pd.read_csv('C:/Users/Emma Davidson/PycharmProjects/sign-language-interpreter/data/sign_mnist_train/sign_mnist_train.csv')
test_df = pd.read_csv('C:/Users/Emma Davidson/PycharmProjects/sign-language-interpreter/data/sign_mnist_test/sign_mnist_test.csv')

# Separate features and labels
y_train = train_df['label']
X_train = train_df.drop('label', axis=1)

y_test = test_df['label']
X_test = test_df.drop('label', axis=1)

# ---------------------------
# 2. Preprocess Data
# ---------------------------
# Reshape and normalize
X_train = X_train.values.reshape(-1, 28, 28, 1).astype('float32') / 255.0
X_test = X_test.values.reshape(-1, 28, 28, 1).astype('float32') / 255.0

# One-hot encode labels
label_bin = LabelBinarizer()
y_train = label_bin.fit_transform(y_train)
y_test = label_bin.transform(y_test)

# ---------------------------
# 3. Data Augmentation (optional, simplify first)
# ---------------------------
train_datagen = ImageDataGenerator()

# ---------------------------
# 4. Build Model
# ---------------------------
model = Sequential([
    Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(256, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.1),
    Dense(24, activation='softmax')  # A-Y excluding J & Z
])

# ---------------------------
# 5. Compile Model
# ---------------------------
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# ---------------------------
# 6. Train Model
# ---------------------------
history = model.fit(
    train_datagen.flow(X_train, y_train, batch_size=64),
    epochs=15,
    validation_data=(X_test, y_test)
)

# ---------------------------
# 7. Evaluate Model
# ---------------------------
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print("\n✅ Test accuracy:", test_accuracy)

# ---------------------------
# 8. Confusion Matrix
# ---------------------------
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

# ---------------------------
# 9. Classification Report
# ---------------------------
print(classification_report(y_true, y_pred_classes))

# ---------------------------
# 10. Save Model
# ---------------------------
model.save('asl_model_improved.h5')
print("✅ Model saved as asl_model_debugged.h5")
