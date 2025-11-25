import os
import numpy as np
from sklearn.model_selection import train_test_split

PROCESSED_DIR = "data/processed"

CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']

def load_processed_data():
    X, y = [], []

    train_dir = os.path.join(PROCESSED_DIR, "Train")

    for class_index, class_name in enumerate(CLASSES):
        class_folder = os.path.join(train_dir, class_name)
        for file in os.listdir(class_folder):
            if file.endswith(".npy"):
                arr = np.load(os.path.join(class_folder, file))
                X.append(arr)
                y.append(class_index)

    X = np.array(X)
    y = np.array(y)

    return train_test_split(X, y, test_size=0.2, random_state=42)