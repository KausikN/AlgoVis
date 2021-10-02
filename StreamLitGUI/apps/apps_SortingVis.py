"""
Stream lit GUI for SortingVis
"""

# Imports
# import os
# import cv2
# import streamlit as st
# import json
# import subprocess
# import functools

from Algorithms import SortingVis

#############################################################################################################################
# Repo Based Vars
SortingVis_SORT_FUNCS = SortingVis.SORT_ALGORITHMS

# Util Vars


# Util Functions


# Main Functions


# UI Functions
def UI_DisplaySortingOutput(array, array_sorted, trace):
    # Title
    st.markdown("## Sort Output")

    colsize = (1, 3)
    
    col1, col2 = st.columns(colsize)
    col1.markdown("Input Array")
    col2.markdown("```python\n" + str(array))

    col1, col2 = st.columns(colsize)
    col1.markdown("Sorted Array")
    col2.markdown("```python\n" + str(array_sorted))

    col1, col2 = st.columns(colsize)
    col1.markdown("Number of Swaps")
    col2.markdown("```python\n" + str(len(trace)) + " swaps")

    # Display Video
    FixSavedVideoFile()
    VideoData = open(DEFAULT_SAVEPATH_VIDEO_CONVERTED, 'rb').read()
    st.video(VideoData)

# Repo Based Functions
def sort_algorithms():
    # Title
    st.header("Sort Algorithms")

    # Prereq Loaders

    # Load Inputs
    SORT_FUNCS_NAMES = list(SortingVis_SORT_FUNCS.keys())
    USERINPUT_SortAlgoName = st.selectbox("Select Sort Algorithm", SORT_FUNCS_NAMES)

    USERINPUT_ArraySize = st.slider("Select Array Size", 5, 100, 25, 5)

    DEFAULT_VIDEO_DURATION = st.number_input("Select Video Duration", 0.5, 10.0, 2.0, 0.5)

    # Process Inputs
    if st.button("Visualise"):
        USERINPUT_SortFunc = SortingVis_SORT_FUNCS[USERINPUT_SortAlgoName]

        # Generate Array
        array = SortingVis.GenerateArray_Random(USERINPUT_ArraySize)

        # Visualise Array
        array_sorted, trace = SortingVis.SortVis_PlotGIF(USERINPUT_SortFunc, array, DEFAULT_SAVEPATH_VIDEO, duration=DEFAULT_VIDEO_DURATION)
        
        # Display Outputs
        UI_DisplaySortingOutput(array, array_sorted, trace)
    
#############################################################################################################################
# Driver Code