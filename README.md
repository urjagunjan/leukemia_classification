# Leukemia Cell Classification - Interactive Dashboard

## Project Overview

This project provides an interactive data analytics dashboard for exploring a leukemia cell image dataset. It allows users to visualize dataset statistics, class distributions, and browse sample images for different types of blood cells, aiding in the initial stages of a leukemia classification task.

The dashboard is built using Python with Streamlit, Pandas for data manipulation, and Matplotlib for visualizations.

## Dataset

- **Source**: Kaggle - [Blood Cell Images (Leukemia Classification)](https://www.kaggle.com/datasets/paultimothymooney/blood-cells)
- **Contents**: Over 12,000 images of blood cells, categorized into four types: EOSINOPHIL, LYMPHOCYTE, MONOCYTE, and NEUTROPHIL.
- **Structure**: The dataset is typically organized into `TRAIN` and `TEST` subdirectories, each containing folders for the respective cell types.

## Features

- **Interactive Dashboard**: User-friendly interface built with Streamlit.
- **Data Loading**: Automatically downloads and processes the Kaggle dataset (requires Kaggle API key).
- **Dataset Overview Tab**:
    - Displays total image counts (overall and by TRAIN/TEST split).
    - Visualizes class distribution with a bar chart for the selected split (ALL, TRAIN, or TEST).
    - Shows a pie chart for TRAIN vs. TEST split distribution.
- **Image Explorer Tab**:
    - Allows browsing of sample images for each cell type.
    - Customizable number of samples to display.
    - Filters images by TRAIN, TEST, or ALL splits.
    - Displays image captions with filename, label, split, and truncated filepath.
- **Sidebar Controls**: Easy-to-use controls for setting the image directory path, selecting data splits, and choosing the number of sample images.

## Setup and Installation

1.  **Clone the Repository (or Download Files)**:
    Ensure you have all the project files (`dashboard.py`, `data_loader.py`, `requirements.txt`).

2.  **Create a Python Environment (Recommended)**:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install Dependencies**:
    Navigate to the project directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Kaggle API Key**:
    - Go to your Kaggle account page: [https://www.kaggle.com/](https://www.kaggle.com/) -> (Your Profile Icon) -> Account.
    - Scroll down to the "API" section and click "Create New API Token". This will download a `kaggle.json` file.
    - Place the `kaggle.json` file in the required directory:
        - On Windows: `C:\Users\<Your-Username>\.kaggle\kaggle.json`
        - On macOS/Linux: `~/.kaggle/kaggle.json`
    - Ensure the `.kaggle` directory exists; create it if it doesn't.

## How to Run

1.  **Download and Prepare Data (First Time)**:
    Run the `data_loader.py` script once to download the dataset from Kaggle and prepare the image list. Make sure your Kaggle API key is set up.
    ```bash
    python data_loader.py
    ```
    This will create a `./kaggle_data` directory for the downloaded zip and a `./blood_cell_images` directory for the extracted images.

2.  **Launch the Streamlit Dashboard**:
    Once the data is ready, run the dashboard application:
    ```bash
    python -m streamlit run dashboard.py
    ```
    - The first time you run Streamlit, it might ask for an email. You can leave it blank and press Enter.
    - The dashboard will typically be available at `http://localhost:8501` in your web browser.

## File Structure

```
leukemia_classification/
├── .venv/                          # Virtual environment (optional)
├── blood_cell_images/              # Extracted image data (created by data_loader.py)
│   └── dataset2-master/
│       └── dataset2-master/
│           └── images/
│               ├── TEST/
│               │   ├── EOSINOPHIL/
│               │   ├── LYMPHOCYTE/
│               │   ├── MONOCYTE/
│               │   └── NEUTROPHIL/
│               └── TRAIN/
│                   ├── EOSINOPHIL/
│                   ├── LYMPHOCYTE/
│                   ├── MONOCYTE/
│                   └── NEUTROPHIL/
├── kaggle_data/                    # Downloaded Kaggle zip files (created by data_loader.py)
├── dashboard.py                    # Main Streamlit dashboard application
├── data_loader.py                  # Script for downloading and preparing data
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Customization

- **Image Path**: The default image path in the dashboard is `./blood_cell_images/dataset2-master/dataset2-master/images`. You can change this in the sidebar if your images are located elsewhere.
- **Further Analysis**: This project serves as a starting point. You can extend it by adding more sophisticated EDA, image preprocessing, feature extraction, and machine learning models for classification.
