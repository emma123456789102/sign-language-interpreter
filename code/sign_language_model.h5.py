import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import sklearn
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils.class_weight import compute_class_weight

# Define image size and batch size
IMG_SIZE = (64, 64)
BATCH_SIZE = 32
COLOR_MODE = 'grayscale'  # Change to 'rgb' if dataset has colored images
INPUT_SHAPE = (64, 64, 1) if COLOR_MODE == 'grayscale' else (64, 64, 3)

# Data paths (Update these if necessary)
TRAIN_DIR = "./dataset/ASL-Alphabet-Dataset-main/data/train"
TEST_DIR = "./dataset/ASL-Alphabet-Dataset-main/data/test"

# Check if dataset directories exist
if not os.path.exists(TRAIN_DIR) or not os.path.exists(TEST_DIR):
    raise FileNotFoundError(f"Dataset directories not found! Please check the paths:\nTrain: {TRAIN_DIR}\nTest: {TEST_DIR}")

# Ensure the dataset has subdirectories (each representing a class)
if not any(os.path.isdir(os.path.join(TRAIN_DIR, d)) for d in os.listdir(TRAIN_DIR)):
    raise ValueError("Training directory should contain subdirectories for each class.")

if not any(os.path.isdir(os.path.join(TEST_DIR, d)) for d in os.listdir(TEST_DIR)):
    raise ValueError("Test directory should contain subdirectories for each class.")

# Print dataset structure
print("Classes in Train Directory:", os.listdir(TRAIN_DIR))
print("Classes in Test Directory:", os.listdir(TEST_DIR))

# Data augmentation and preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.3,
    zoom_range=0.4,
    horizontal_flip=True,
    validation_split=0.4  # Now using 60% train, 40% validation
)

test_datagen = ImageDataGenerator(rescale=1./255)  # No augmentation for test set

# Load training data
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    color_mode=COLOR_MODE,
    class_mode='categorical',
    subset='training'
)

# Load validation data
valid_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    color_mode=COLOR_MODE,
    class_mode='categorical',
    subset='validation'
)

# Load test data
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    color_mode=COLOR_MODE,
    class_mode='categorical',
    shuffle=False
)

# Compute class weights for imbalance handling
class_labels = list(train_generator.class_indices.keys())
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(train_generator.classes),
    y=train_generator.classes
)
class_weights_dict = dict(enumerate(class_weights))

print("Class Weights:", class_weights_dict)

# Get number of classes dynamically
num_classes = len(train_generator.class_indices)

# Build the CNN model with Batch Normalization & Dropout
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=INPUT_SHAPE),
    BatchNormalization(),
    MaxPooling2D(2,2),
    Dropout(0.3),  # Improved dropout

    Conv2D(64, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2,2),
    Dropout(0.4),

    Conv2D(128, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2,2),
    Dropout(0.5),

    Flatten(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),  # Stronger dropout
    Dense(num_classes, activation='softmax')
])

# Compile the model with lower learning rate
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-4)  # Slower learning rate
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with class weights
EPOCHS = 15
history = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=EPOCHS,
    class_weight=class_weights_dict  # Apply class weights
)

# Save the model
model.save("sign_language_model.h5")
print("Model training complete and saved as sign_language_model.h5")

# Evaluate on test set
test_loss, test_acc = model.evaluate(test_generator)
print(f"Test Accuracy: {test_acc:.4f}, Test Loss: {test_loss:.4f}")

# Plot accuracy and loss graphs
def plot_history(history):
    # Accuracy plot
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Model Accuracy')
    plt.legend()
    plt.grid(True)

    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Model Loss')
    plt.legend()
    plt.grid(True)

    plt.show()

# Call the function to plot
plot_history(history)
