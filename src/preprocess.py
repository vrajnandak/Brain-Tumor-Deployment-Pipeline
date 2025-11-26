import os
import cv2
import numpy as np

IMAGE_SIZE = 128

RAW_DIR_TRAIN = "data/raw/Training"
RAW_DIR_TEST  = "data/raw/Testing"
PROCESSED_DIR = "data/processed"

def preprocess_image(img_path):
    img = cv2.imread(img_path)

    if img is None:
        print(f"WARNING: Skipping unreadable file: {img_path}")
        return None

    img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
    img = img / 255.0
    return img

def process_split(split_raw_path, split_processed_path):
    os.makedirs(split_processed_path, exist_ok=True)

    for class_name in os.listdir(split_raw_path):
        class_raw_path = os.path.join(split_raw_path, class_name)

        # Skip non-folders (safety check)
        if not os.path.isdir(class_raw_path):
            continue

        class_out_path = os.path.join(split_processed_path, class_name)
        os.makedirs(class_out_path, exist_ok=True)

        for file in os.listdir(class_raw_path):
            if file.lower().endswith((".jpg", ".png", ".jpeg")):

                img_path = os.path.join(class_raw_path, file)
                img = preprocess_image(img_path)

                if img is None:
                    continue

                # safer name: file.jpg → file.npy
                base_name, _ = os.path.splitext(file)
                save_path = os.path.join(class_out_path, base_name + ".npy")

                np.save(save_path, img)

        print(f"Processed class: {class_name}")

def run_preprocessing():
    print("Starting preprocessing...")

    process_split(RAW_DIR_TRAIN, os.path.join(PROCESSED_DIR, "Train"))
    process_split(RAW_DIR_TEST,  os.path.join(PROCESSED_DIR, "Test"))

    print("Preprocessing completed!")

if __name__ == "__main__":
    run_preprocessing()
