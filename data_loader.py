import os
import zipfile
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def download_and_extract_kaggle_dataset(dataset_name, download_path, extract_path):
    api = KaggleApi()
    api.authenticate()
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    api.dataset_download_files(dataset_name, path=download_path, unzip=False)
    zip_files = [f for f in os.listdir(download_path) if f.endswith('.zip')]
    for zip_file in zip_files:
        with zipfile.ZipFile(os.path.join(download_path, zip_file), 'r') as zip_ref:
            zip_ref.extractall(extract_path)

def create_image_dataframe(base_image_dir):
    data = []
    # Iterate over TRAIN, TEST subdirectories (and TEST_SIMPLE if desired)
    for split_folder_name in ["TRAIN", "TEST"]:
        split_folder_path = os.path.join(base_image_dir, split_folder_name)
        if not os.path.isdir(split_folder_path):
            print(f"Warning: Subfolder {split_folder_path} not found or not a directory.")
            continue

        for label in os.listdir(split_folder_path):  # These should be the class labels like EOSINOPHIL
            label_path = os.path.join(split_folder_path, label)
            if os.path.isdir(label_path):
                for img_file in os.listdir(label_path):
                    if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        data.append({'filepath': os.path.join(label_path, img_file),
                                     'label': label,
                                     'split': split_folder_name})  # Add split info
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    DATASET = "paultimothymooney/blood-cells"
    DOWNLOAD_PATH = "./kaggle_data"
    EXTRACT_PATH = "./blood_cell_images"
    # download_and_extract_kaggle_dataset(DATASET, DOWNLOAD_PATH, EXTRACT_PATH) # Already downloaded
    base_img_dir_path = os.path.join(EXTRACT_PATH, "dataset2-master/dataset2-master/images")
    df = create_image_dataframe(base_img_dir_path)
    print("DataFrame created by data_loader.py:")
    print(df.head())
    print(f"Total images loaded: {len(df)}")
    if not df.empty:
        print("\nClass distribution:")
        print(df['label'].value_counts())
        print("\nSplit distribution:")
        print(df['split'].value_counts())
