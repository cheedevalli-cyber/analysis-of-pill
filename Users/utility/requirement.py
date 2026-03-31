import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # must be before pyplot
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.layers import Dropout, Input, Dense, BatchNormalization, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.models import Model
from django.conf import settings

##########################
# Data Loading Functions
##########################

def load_data(train_csv_path, test_csv_path):
    """Load the training and testing datasets from CSV files."""
    train_df = pd.read_csv(train_csv_path)
    test_df = pd.read_csv(test_csv_path)
    
    train_df['label'] = pd.Categorical(train_df['label']).codes
    test_df['label'] = pd.Categorical(test_df['label']).codes
    return train_df, test_df

def check_data_balance(train_df):
    sns.histplot(train_df['label'])
    plt.title("Distribution of Training Labels")
    plt.savefig("label_distribution.png")
    plt.close()


def preprocess_images(file_paths, base_path, target_size=(64, 64)):
    """Preprocess images by loading and resizing them."""
    images = []
    for file in file_paths:
        img_path = base_path / file
        img = load_img(img_path, color_mode='grayscale')
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        img = np.array(img)
        images.append(img)
    return np.array(images)

##########################
# Model Functions
##########################

def build_model(input_shape, num_classes):
    inputs = Input(input_shape)
    X = Conv2D(64, (3, 3), activation='relu', kernel_initializer=glorot_uniform(seed=0))(inputs)
    X = BatchNormalization(axis=3)(X)
    X = MaxPooling2D((3, 3))(X)

    X = Conv2D(128, (3, 3), activation='relu')(X)
    X = MaxPooling2D((2, 2))(X)

    X = Conv2D(256, (3, 3), activation='relu')(X)
    X = MaxPooling2D((2, 2))(X)

    X = Flatten()(X)

    dense_1 = Dense(256, activation='relu')(X)
    dropout_1 = Dropout(0.4)(dense_1)

    dense_2 = Dense(128, activation='relu')(dropout_1)
    dropout_2 = Dropout(0.4)(dense_2)

    output = Dense(num_classes, activation='softmax', name='pill_output')(dropout_2)

    model = Model(inputs=[inputs], outputs=[output])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

def plot_history(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.legend(['train', 'validation'])
    plt.savefig("accuracy.png")
    plt.close()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.legend(['train', 'validation'])
    plt.savefig("loss.png")
    plt.close()


def evaluate_model(model, x_test, y_test):
    y_pred = np.argmax(model.predict(x_test), axis=-1)
    pill_report = classification_report(y_test, y_pred)
    pill_accuracy = accuracy_score(y_test, y_pred)
    print("Pill Identification Classification Report:\n", pill_report)
    print("Pill Identification Accuracy: {:.2f}%".format(pill_accuracy * 100))
    return pill_accuracy

##########################
# Main Training Function
##########################

def main():
    """Train model and save it to MEDIA_ROOT."""
    # Paths inside MEDIA_ROOT
    pilldata_dir = Path(settings.MEDIA_ROOT) / 'pilldata'
    train_csv_path = pilldata_dir / 'Training_set.csv'
    test_csv_path = pilldata_dir / 'Testing_set.csv'
    train_path = pilldata_dir / 'train'
    model_path = pilldata_dir / 'model.h5'

    # Load data
    train_df, test_df = load_data(train_csv_path, test_csv_path)
    check_data_balance(train_df)

    # Preprocess images
    x_train = preprocess_images(train_df['filename'], train_path)
    x_train = x_train.reshape(len(x_train), 64, 64, 1) / 255.0
    y_train = np.array(train_df['label'], dtype=np.int32)

    x_train, x_test, y_train, y_test = train_test_split(
        x_train, y_train, test_size=0.1, random_state=39, stratify=y_train
    )

    # Build and train model
    input_size = (64, 64, 1)
    model = build_model(input_size, len(train_df['label'].unique()))
    history = model.fit(x_train, y_train, batch_size=32, epochs=10, validation_split=0.1)

    # Save model
    model.save(model_path)
    plot_history(history)

    # Evaluate
    pill_accuracy = evaluate_model(model, x_test, y_test)
    return pill_accuracy

##########################
# Prediction Functions
##########################

def preprocess_image(image_path):
    """Preprocess a single image for prediction."""
    img = load_img(image_path, color_mode='grayscale')
    img = img.resize((64, 64), Image.Resampling.LANCZOS)
    img = np.array(img) / 255.0
    img = img.reshape(1, 64, 64, 1)  # Add batch dimension
    return img

def predict_pill(pred):
    pred_class = int(np.argmax(pred, axis=-1)[0])
    label_map = {
        0: 'Alaxan', 1: 'Bactidol', 2: 'Bioflu', 3: 'Biogesic', 4: 'DayZinc',
        5: 'Decolgen', 6: 'Fish Oil', 7: 'Kremil S', 8: 'Medicol', 9: 'Neozep'
    }
    return label_map.get(pred_class, "Unknown")

# Global variable to cache the loaded model to save memory and reduce loading time
_model_cache = None

def predictions(image_path):
    """Predict a pill class using the saved model in MEDIA_ROOT."""
    global _model_cache

    if _model_cache is None:
        pilldata_dir = Path(settings.MEDIA_ROOT) / 'pilldata'
        model_path = pilldata_dir / 'model.h5'

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")

        # Loading the model with compile=False saves memory and speeds up prediction
        _model_cache = load_model(model_path, compile=False)

    processed_image = preprocess_image(image_path)
    # Perform prediction
    val = _model_cache.predict(processed_image)
    predicted_label = predict_pill(val)
    
    import cv2
    try:
        img_str = str(image_path)
        img = cv2.imread(img_str)
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply a strong blur to remove texture noise
            blurred = cv2.GaussianBlur(gray, (11, 11), 0)
            
            # Canny with broader thresholds
            edges = cv2.Canny(blurred, 20, 80)
            
            # Strong dilation to connect all pill-related edges into a solid mass
            kernel = np.ones((7,7), np.uint8)
            dilated = cv2.dilate(edges, kernel, iterations=3)
            
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            best_pill = None
            min_dist = float('inf')
            img_h, img_w = img.shape[:2]
            img_center = (img_w // 2, img_h // 2)
            
            for c in contours:
                area = cv2.contourArea(c)
                # Reasonable pill area range
                if 500 < area < (img_w * img_h * 0.5):
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        dist = np.sqrt((cx - img_center[0])**2 + (cy - img_center[1])**2)
                        
                        if dist < min_dist:
                            min_dist = dist
                            best_pill = c
            
            # Fallback to largest contour if no central pill is found
            if best_pill is None and contours:
                best_pill = max(contours, key=cv2.contourArea)
            
            if best_pill is not None:
                ((x, y), radius) = cv2.minEnclosingCircle(best_pill)
                center = (int(x), int(y))
                # Use a generous radius to fully encompass the tablet
                # thickness 4 for high visibility
                cv2.circle(img, center, int(radius) + 15, (0, 0, 255), 4)
            
            cv2.imwrite(img_str, img)
    except Exception as e:
        print(f"Error drawing circle: {e}")

    return predicted_label
