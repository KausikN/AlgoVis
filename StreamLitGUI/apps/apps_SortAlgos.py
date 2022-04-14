"""
Stream lit GUI for Sort Algorithms
"""

# Imports
# import os
# import cv2
# import streamlit as st
# import json
# import subprocess
# import functools

from Algorithms.SortAlgos.SortingVis import *

# Main Functions
def main_SortAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose Sort Algorithm',
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
    VideoUtils.FixVideoFile(DEFAULT_SAVEPATH_VIDEO, DEFAULT_SAVEPATH_VIDEO_CONVERTED)
    VideoData = open(DEFAULT_SAVEPATH_VIDEO_CONVERTED, 'rb').read()
    st.video(VideoData)

# Repo Based Functions
def sort_algorithms():
    global DEFAULT_VIDEO_DURATION

    # Title
    st.header("Sort Algorithms")

    # Prereq Loaders

    # Load Inputs
    SORT_FUNCS_NAMES = list(SORT_ALGORITHMS.keys())
    USERINPUT_SortAlgoName = st.selectbox("Select Sort Algorithm", SORT_FUNCS_NAMES)

    USERINPUT_ArraySize = st.slider("Select Array Size", 5, 100, 25, 5)

    # DEFAULT_VIDEO_DURATION = st.number_input("Select Video Duration", 0.5, 10.0, 2.0, 0.5)

    # Process Inputs
    if st.button("Visualise"):
        USERINPUT_SortFunc = SORT_ALGORITHMS[USERINPUT_SortAlgoName]

        # Generate Array
        array = GenerateArray_Random(USERINPUT_ArraySize)

        # Visualise Array
        array_sorted, trace = SortVis_PlotGIF(USERINPUT_SortFunc, array, DEFAULT_SAVEPATH_VIDEO, duration=DEFAULT_VIDEO_DURATION)
        
        # Display Outputs
        UI_DisplaySortingOutput(array, array_sorted, trace)
    
#############################################################################################################################
# Driver Code
main_SortAlgos()