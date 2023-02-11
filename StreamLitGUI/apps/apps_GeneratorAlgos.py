"""
Stream lit GUI for Generator Algorithms
"""

# Imports
# import os
# import cv2
import streamlit as st
# import json
# import subprocess
# import functools

from Algorithms.GeneratorAlgos.RandomGenerator import *

# Main Functions
def main_GeneratorAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose Generator Algorithm',
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
def UI_RandomFrequencyDistribution():
    USERINPUT_numRange = st.slider("Select Random Value Range", 1, 100, (1, 5), 1)
    USERINPUT_nframes = st.number_input("Select Number of Values to Generate", 1, 500, 10, 1)
    USERINPUT_saveFPS = USERINPUT_nframes / DEFAULT_VIDEO_DURATION

    if st.button("Generate"):
        # Process Inputs
        Is = RandomFrequencyDistribution_Vis(USERINPUT_numRange, USERINPUT_nframes, 'Random Frequency Distribution')

        # Display Outputs
        st.markdown("## Generated Random Frequency Distribution")
        VideoUtils.SaveFrames2Video(Is, PATHS["default"]["save"]["video"], USERINPUT_saveFPS)
        VideoUtils.FixVideoFile(PATHS["default"]["save"]["video"], PATHS["default"]["save"]["video_converted"])
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"])

def UI_Random2DPoints():
    col1, col2 = st.columns(2)
    USERINPUT_pointXBounds = col1.slider("Select X Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_pointYBounds = col2.slider("Select Y Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_nframes = st.number_input("Select Number of Points to Generate", 1, 500, 10, 1)
    USERINPUT_saveFPS = USERINPUT_nframes / DEFAULT_VIDEO_DURATION

    if st.button("Generate"):
        # Process Inputs
        Is = Random2DPointsGenerator_Vis([USERINPUT_pointXBounds, USERINPUT_pointYBounds], USERINPUT_nframes, 'Random 2D Points')

        # Display Outputs
        st.markdown("## Generated Random 2D Points")
        VideoUtils.SaveFrames2Video(Is, PATHS["default"]["save"]["video"], USERINPUT_saveFPS)
        VideoUtils.FixVideoFile(PATHS["default"]["save"]["video"], PATHS["default"]["save"]["video_converted"])
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"])

def UI_Random3DPoints():
    col1, col2, col3 = st.columns(3)
    USERINPUT_pointXBounds = col1.slider("Select X Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_pointYBounds = col2.slider("Select Y Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_pointZBounds = col3.slider("Select Z Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_nframes = st.number_input("Select Number of Points to Generate", 1, 500, 10, 1)
    USERINPUT_saveFPS = USERINPUT_nframes / DEFAULT_VIDEO_DURATION

    if st.button("Generate"):
        # Process Inputs
        Is = Random3DPointsGenerator_Vis([USERINPUT_pointXBounds, USERINPUT_pointYBounds, USERINPUT_pointZBounds], USERINPUT_nframes, 'Random 3D Points')

        # Display Outputs
        st.markdown("## Generated Random 3D Points")
        VideoUtils.SaveFrames2Video(Is, PATHS["default"]["save"]["video"], USERINPUT_saveFPS)
        VideoUtils.FixVideoFile(PATHS["default"]["save"]["video"], PATHS["default"]["save"]["video_converted"])
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"])

RANDOMGENERATOR_VISUALISAITON_MAP = {
    "Random Frequency Distribution": UI_RandomFrequencyDistribution,
    "Random 2D Points": UI_Random2DPoints,
    "Random 3D Points": UI_Random3DPoints
}

# Repo Based Functions
def random_generators():
    # Title
    st.header("Random Generators")

    # Load Inputs
    USERINPUT_VisChoice = st.selectbox("Select Visualization Type", list(RANDOMGENERATOR_VISUALISAITON_MAP.keys()))

    # Process Inputs
    RANDOMGENERATOR_VISUALISAITON_MAP[USERINPUT_VisChoice]()
    
#############################################################################################################################
# Driver Code
main_GeneratorAlgos()