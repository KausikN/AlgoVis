"""
Stream lit GUI for Clustering Algorithms
"""

# Imports
# import os
# import cv2
# import streamlit as st
# import json
# import subprocess
# import functools

from Algorithms.ClusteringAlgos import KMeansClustering

# Main Functions
def main_ClusteringAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose Clustering Algorithm',
        tuple(
            SUBAPP_MODES
        )
    )

    # Add Functions
    correspondingFuncName = selected_box.replace(' ', '_').lower()
    if correspondingFuncName in globals().keys():
        globals()[correspondingFuncName]()

#############################################################################################################################
# Repo Based Vars
KMEANS_DIM_OPTIONS = ["1D", "2D", "3D"]

# Util Vars


# Util Functions


# Main Functions


# UI Functions


# Repo Based Functions
def kmeans_clustering():
    global DEFAULT_VIDEO_DURATION

    # Title
    st.header("K-Means Clustering")

    # Prereq Loaders

    # Load Inputs
    st.markdown("## Data Generation Inputs")
    col1, col2 = st.columns(2)
    USERINPUT_N = col1.number_input("Number of Points", 2, 10000, 3, 1)
    USERINPUT_DIM = col2.selectbox("Data Dimensions", KMEANS_DIM_OPTIONS)

    st.markdown("## KMeans Inputs")
    col1, col2, col3 = st.columns(3)
    USERINPUT_K = col1.number_input("Enter K", 1, 100, 3, 1)
    USERINPUT_max_iters = col2.number_input("Enter Iteration Count", 1, 100, 10, 1)
    USERINPUT_cluster_count = col3.number_input("Enter Clusters Count", 1, 100, 3, 1)

    # Process Inputs
    USERINPUT_DIM = int(KMEANS_DIM_OPTIONS.index(USERINPUT_DIM)) + 1
    if st.button("Visualise"):
        # Generate Dataset
        Dataset = KMeansClustering.DatasetGenerators.GenerateRandomBlobs(
            N=USERINPUT_N, dim=USERINPUT_DIM, centers=USERINPUT_cluster_count, plot=False
        )
        # print(Dataset)
        # Run KMeans
        Results = KMeansClustering.KMeansClustering(Dataset, USERINPUT_K, USERINPUT_max_iters)
        # print(Results)
        # Save Animation
        KMeansClustering.Animate_KMeansConvergence(Dataset, Results, DEFAULT_SAVEPATH_VIDEO, duration=DEFAULT_VIDEO_DURATION)
        KMeansClustering.VideoUtils.FixVideoFile(DEFAULT_SAVEPATH_VIDEO, DEFAULT_SAVEPATH_VIDEO_CONVERTED)
        # Display Animation Video
        st.video(DEFAULT_SAVEPATH_VIDEO_CONVERTED) 
    
#############################################################################################################################
# Driver Code
main_ClusteringAlgos()