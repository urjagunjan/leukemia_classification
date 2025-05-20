import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np # For color generation

def load_data(base_image_dir):
    data = []
    for split_folder_name in ["TRAIN", "TEST"]:
        split_folder_path = os.path.join(base_image_dir, split_folder_name)
        if not os.path.isdir(split_folder_path):
            # print(f"Warning: Subfolder {split_folder_path} not found or not a directory.") # Less verbose in dashboard
            continue
        for label in os.listdir(split_folder_path):
            label_path = os.path.join(split_folder_path, label)
            if os.path.isdir(label_path):
                for img_file in os.listdir(label_path):
                    if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        data.append({'filepath': os.path.join(label_path, img_file),
                                     'label': label,
                                     'split': split_folder_name})
    df = pd.DataFrame(data)
    if df.empty:
        st.error(f"No images found. Searched in {base_image_dir}/TRAIN and {base_image_dir}/TEST. Please check the path and directory structure.")
    return df

def main():
    st.set_page_config(layout="wide") # Use wider layout
    st.title("Leukemia Cell Classification Dashboard")

    # --- Sidebar for Controls ---
    st.sidebar.header("Dashboard Controls")
    image_dir_default = "./blood_cell_images/dataset2-master/dataset2-master/images"
    image_dir = st.sidebar.text_input("Path to Image Directory:", image_dir_default)

    if not os.path.exists(image_dir) or not os.path.isdir(image_dir):
        st.error(f"Image directory not found: {image_dir}. Please ensure the path is correct and contains TRAIN/TEST subfolders.")
        return

    df_full = load_data(image_dir)
    if df_full.empty:
        return # load_data will show an error

    split_option = st.sidebar.selectbox("Select Data Split:", ["ALL", "TRAIN", "TEST"], index=0)
    num_samples_per_class = st.sidebar.number_input("Sample Images per Class:", min_value=1, max_value=10, value=3)

    # Filter dataframe based on selected split
    if split_option == "ALL":
        df_display = df_full
    else:
        df_display = df_full[df_full['split'] == split_option]

    if df_display.empty and split_option != "ALL":
        st.warning(f"No images found for the '{split_option}' split.")
        # Fallback to all data if selected split is empty to prevent errors, but show warning
        df_display = df_full 

    # --- Main Panel with Tabs ---
    tab1, tab2 = st.tabs(["📊 Dataset Overview", "🖼️ Image Explorer"])

    with tab1:
        st.header(f"Dataset Overview - {split_option} Split")
        if df_display.empty:
            st.warning("No data to display for the current selection.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Images in Selection", len(df_display))
                if split_option == "ALL":
                    st.metric("Total Images (TRAIN)", len(df_full[df_full['split'] == 'TRAIN']))
                    st.metric("Total Images (TEST)", len(df_full[df_full['split'] == 'TEST']))
            
            with col2:
                if split_option == "ALL" and not df_full.empty:
                    st.subheader("Overall Split Distribution")
                    split_counts = df_full['split'].value_counts()
                    fig_split, ax_split = plt.subplots(figsize=(5,4))
                    ax_split.pie(split_counts, labels=split_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
                    ax_split.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
                    st.pyplot(fig_split)
                elif split_option != "ALL":
                    st.info(f"Displaying data for '{split_option}' split only.")

            st.subheader("Class Distribution")
            if not df_display.empty:
                class_counts = df_display['label'].value_counts()
                fig_class, ax_class = plt.subplots()
                # Generate more distinct colors for potentially more classes
                colors = plt.cm.get_cmap('viridis', len(class_counts))(np.linspace(0, 1, len(class_counts)))
                class_counts.plot(kind='bar', color=colors, ax=ax_class)
                ax_class.set_title(f"Class Distribution in '{split_option}' Split")
                ax_class.set_ylabel("Number of Images")
                ax_class.set_xlabel("Cell Type")
                plt.xticks(rotation=45, ha='right')
                st.pyplot(fig_class)
            else:
                st.write("No class data to display for this selection.")

    with tab2:
        st.header(f"Image Explorer - {split_option} Split")
        if df_display.empty:
            st.warning("No images to display for the current selection.")
        else:
            unique_labels = sorted(df_display['label'].unique())
            for label in unique_labels:
                st.subheader(f"Sample Images: {label}")
                sample_df = df_display[df_display['label'] == label].sample(min(num_samples_per_class, len(df_display[df_display['label'] == label])))
                if sample_df.empty:
                    st.write(f"No '{label}' images found in the '{split_option}' split.")
                    continue
                
                # Dynamically create columns based on num_samples_per_class
                cols = st.columns(num_samples_per_class)
                for idx, row_data in enumerate(sample_df.itertuples()):
                    img = Image.open(row_data.filepath)
                    with cols[idx % num_samples_per_class]: # Ensure we don't go out of bounds if less samples than num_samples_per_class
                        st.image(img, caption=f"{os.path.basename(row_data.filepath)}\n{label} ({row_data.split})", use_container_width=True)
                        st.caption(f"Path: ...{row_data.filepath[-50:]}") # Show truncated path

if __name__ == "__main__":
    main()
