"""
Stream lit GUI for Random Generator
"""

# Imports
# import os
# import cv2
# import streamlit as st
# import json
# import subprocess
# import functools

from Algorithms import RandomGenerator

#############################################################################################################################
# Repo Based Vars


# Util Vars


# Util Functions


# Main Functions


# UI Functions


# Repo Based Functions
def random_generators():
    # Title
    st.header("Random Generators")

    # Load Inputs
    USERINPUT_numRange = st.slider("Select Random Value Range", 1, 100, (1, 5), 1)
    USERINPUT_nframes = st.number_input("Select Number of Values to Generate", 1, 500, 10, 1)
    USERINPUT_frameLim = (0, 1)
    USERINPUT_saveFPS = USERINPUT_nframes / st.number_input("Select Animation Duration", 0.1, 2.5, 1.0, 0.1)

    if st.button("Generate"):
        # Process Inputs
        animation = RandomGenerator.RandomGenerator_Vis(USERINPUT_numRange, USERINPUT_frameLim, USERINPUT_nframes, False)

        # Display Outputs
        st.markdown("## Generated Random Distribution")
        RandomGenerator.PAL.SavePlotGIF(animation, DEFAULT_SAVEPATH_GIF, USERINPUT_saveFPS)
        st.image(DEFAULT_SAVEPATH_GIF, "Generated Random Numbers", use_column_width=True)
    
#############################################################################################################################
# Driver Code