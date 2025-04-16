import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Load the dataset
train_df = pd.read_csv("C:/Users/Emma Davidson/PycharmProjects/sign-language-interpreter/data/sign_mnist_test.csv")
test_df = pd.read_csv("C:/Users/Emma Davidson/PycharmProjects/sign-language-interpreter/data/sign_mnist_test.csv")

# Separate labels and features
x_train = train_df.iloc[:, 1:].values
y_train = train_df.iloc[:, 0].values
x_test = test_df.iloc[:, 1:].values
y_test = test_df.iloc[:, 0].values

# Normalize pixel values
x_train = x_train / 255.0
x_test = x_test / 255.0

# Reshape to image format (28x28x1)
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# One-hot encode labels
y_train = to_categorical(y_train, num_classes=25)
y_test = to_categorical(y_test, num_classes=25)

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(25, activation='softmax')  # 25 letters (A–Z minus J)
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

# Save the model
model.save("sign_language_model.h5")

print("✅ Model trained and saved as sign_language_model.h5")
