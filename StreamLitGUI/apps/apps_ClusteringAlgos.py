"""
Stream lit GUI for Clustering Algorithms
"""

# Imports
# import os
import cv2
# import numpy as np
import streamlit as st
# import json
# import subprocess
# import functools

from Algorithms.ClusteringAlgos.KMeansClustering import *

# Main Functions
def main_ClusteringAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose Clustering Algorithm",
        tuple(
            SUBAPP_MODES
        )
    )

    # Add Functions
    correspondingFuncName = selected_box.replace(" ", "_").lower()
    if correspondingFuncName in globals().keys():
        globals()[correspondingFuncName]()

#############################################################################################################################
# Repo Based Vars
KMEANS_DIM_OPTIONS = ["1D", "2D", "3D"]
DATASET_DEFAULT_PATH_EXAMPLEIMAGE = "StreamLitGUI/DefaultData/ExampleDataset.PNG"
DATASET_LOADTYPES = ["Generate Random", "Load Image"]

# Util Vars


# Util Functions


# Main Functions


# UI Functions
def UI_PointsDatasetLoad():
    
    USERINPUT_DatasetLoadType = st.selectbox("Select Dataset Load Type", DATASET_LOADTYPES)

    DatasetLoader = {"name": "", "func": None, "params": {}}

    # Genrate Random Dataset
    if USERINPUT_DatasetLoadType == DATASET_LOADTYPES[0]:
        col1, col2, col3 = st.columns(3)
        USERINPUT_N = col1.number_input("Number of Points", 2, 10000, 3, 1)
        USERINPUT_DIM = col2.selectbox("Data Dimensions", KMEANS_DIM_OPTIONS)
        USERINPUT_DIM = int(KMEANS_DIM_OPTIONS.index(USERINPUT_DIM)) + 1
        USERINPUT_ClusterCount = col3.number_input("Enter Cluster Count", 1, 100, 3, 1)

        DatasetLoader = {
            "name": "Generate Random",
            "func": DatasetGenerators.GenerateRandomBlobs,
            "params": {"N": USERINPUT_N, "dim": USERINPUT_DIM, "centers": USERINPUT_ClusterCount, "plot": False}
        }

    # Load Image
    elif USERINPUT_DatasetLoadType == DATASET_LOADTYPES[1]:
        
        USERINPUT_ImageData = st.file_uploader("Upload Start Image", ["png", "jpg", "jpeg", "bmp"])
        if USERINPUT_ImageData is not None:
            USERINPUT_ImageData = USERINPUT_ImageData.read()
        else:
            USERINPUT_ImageData = open(DATASET_DEFAULT_PATH_EXAMPLEIMAGE, "rb").read()
        USERINPUT_Image = cv2.imdecode(np.frombuffer(USERINPUT_ImageData, np.uint8), cv2.IMREAD_COLOR)
        USERINPUT_Image = np.array(cv2.cvtColor(USERINPUT_Image, cv2.COLOR_BGR2GRAY))
        col1, col2 = st.columns(2)

        USERINPUT_InvertImage = col1.checkbox("Invert Image", False)
        if USERINPUT_InvertImage:
            USERINPUT_Image = 255 - USERINPUT_Image
        USERINPUT_Threshold = col2.slider("Binarise Threshold", 0, 255, 128, 1)
        USERINPUT_Image = USERINPUT_Image >= USERINPUT_Threshold

        st.image(USERINPUT_Image * 255, caption="Input Image", use_column_width=True)

        DatasetLoader = {
            "name": "Load Image",
            "func": DatasetGenerators.GeneratePointsFromImage,
            "params": {"I": USERINPUT_Image, "plot": False}
        }

    return DatasetLoader

# Repo Based Functions
def kmeans_clustering():
    global DEFAULT_VIDEO_DURATION

    # Title
    st.header("K-Means Clustering")

    # Prereq Loaders

    # Load Inputs
    st.markdown("## Data Generation Inputs")
    DatasetLoader = UI_PointsDatasetLoad()

    st.markdown("## KMeans Inputs")
    col1, col2 = st.columns(2)
    USERINPUT_K = col1.number_input("Enter K", 1, 100, 3, 1)
    USERINPUT_max_iters = col2.number_input("Enter Iteration Count", 1, 100, 10, 1)

    # Process Inputs
    if st.button("Visualise"):
        # Generate Dataset
        Dataset = DatasetLoader["func"](**DatasetLoader["params"])
        # print(Dataset)
        # Run KMeans
        Results = KMeansClustering(Dataset, USERINPUT_K, USERINPUT_max_iters)
        # print(Results)
        # Save Animation
        Animate_KMeansConvergence(Dataset, Results, PATHS["default"]["save"]["video"], duration=DEFAULT_VIDEO_DURATION)
        VideoUtils.FixVideoFile(PATHS["default"]["save"]["video"], PATHS["default"]["save"]["video_converted"])
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"]) 
    
#############################################################################################################################
# Driver Code
main_ClusteringAlgos()