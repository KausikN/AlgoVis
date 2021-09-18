"""
Stream lit GUI for hosting {FEATUREDATA_PROJECT_NAME}
"""

# Imports
import os
import cv2
import streamlit as st
import json
import subprocess
import functools

from Algorithms import SortingVis
from Algorithms import RandomGenerator
from Algorithms import CollatzConjecture

# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config['PROJECT_NAME']] + 
            config['PROJECT_MODES']
        )
    )
    
    if selected_box == config['PROJECT_NAME']:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config['PROJECT_NAME'])
    st.markdown('Github Repo: ' + "[" + config['PROJECT_LINK'] + "](" + config['PROJECT_LINK'] + ")")
    st.markdown(config['PROJECT_DESC'])

    # st.write(open(config['PROJECT_README'], 'r').read())

#############################################################################################################################
# Repo Based Vars
DEFAULT_SAVEPATH_GIF = "StreamLitGUI/DefaultData/SavedGIF.gif"
DEFAULT_SAVEPATH_VIDEO = "StreamLitGUI/DefaultData/SavedVideo.avi"
DEFAULT_SAVEPATH_VIDEO_CONVERTED = "StreamLitGUI/DefaultData/SavedVideo_Converted.mp4"
DEFAULT_VIDEO_DURATION = 2.0

SortingVis_SORT_FUNCS = SortingVis.SORT_ALGORITHMS

# Util Vars
COMMAND_VIDEO_CONVERT = 'ffmpeg -i \"{path_in}\" -vcodec libx264 \"{path_out}\"'

# Util Functions
def GetFunctionsByPrefixName(module, prefixName):
    fnames = [x for x in dir(module) if x.startswith(prefixName)]
    funcs = {}
    for f in fnames:
        funcs[f] = getattr(module, f)
    return funcs

def GetNames(data):
    return [x['name'] for x in data.keys()]

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
    if os.path.exists(DEFAULT_SAVEPATH_VIDEO_CONVERTED):
        os.remove(DEFAULT_SAVEPATH_VIDEO_CONVERTED)

    convert_cmd = COMMAND_VIDEO_CONVERT.format(path_in=DEFAULT_SAVEPATH_VIDEO, path_out=DEFAULT_SAVEPATH_VIDEO_CONVERTED)
    print("Running Conversion Command:")
    print(convert_cmd + "\n")
    ConvertOutput = subprocess.getoutput(convert_cmd)
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

def search_algorithms():
    # Title
    st.header("Search Algorithms")

    st.markdown("In Developement :stuck_out_tongue_winking_eye:")

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

def collatz_conjecture():
    # Title
    st.header("Collatz Conjecture")

    # Load Inputs
    USERINPUT_Mode = st.selectbox("Select Mode", ["Converge Single Value", "Converge Range of Values"])

    if USERINPUT_Mode == "Converge Single Value":
        USERINPUT_startVal = st.number_input("Enter Starting Value", 1, 99999, 23, 1)
        USERINPUT_maxIters = -1
        annotate = False

        if st.button("Visualise"):
            # Process Inputs
            ConvergeFuncSingle = functools.partial(CollatzConjecture.CollatzConjecture_Converge, max_iters=USERINPUT_maxIters)
            trace, iterCount, I_plot = CollatzConjecture.SVL.Series_ValueConvergeVis(ConvergeFuncSingle, USERINPUT_startVal, titles=['Iteration', 'Value', "Collatz Convergence for " + str(USERINPUT_startVal)], annotate=annotate, plot=False)

            # Display Outputs
            st.markdown("## Single Value Trace")
            colSize = (1, 3)
            col1, col2 = st.columns(colSize)
            col1.markdown("Number of Iterations")
            col2.markdown("``` " + str(iterCount) + " ```")
            st.image(I_plot, "Single Value Trace", use_column_width=True)

    if USERINPUT_Mode == "Converge Range of Values":
        USERINPUT_startRange = st.number_input("Enter Range Start", 1, 99999, 23, 1)
        USERINPUT_endRange = st.number_input("Enter Range End", USERINPUT_startRange, 99999, 23, 1)
        USERINPUT_rangeSkip = st.number_input("Enter Range Skip", 1, int((USERINPUT_endRange - USERINPUT_startRange)/2), 1, 1)
        USERINPUT_maxIters = -1

        if st.button("Visualise"):
            # Process Inputs
            computeRange = (USERINPUT_startRange, USERINPUT_endRange, USERINPUT_rangeSkip)
            ConvergeFuncManyValues = functools.partial(CollatzConjecture.CollatzConjecture_Converge, max_iters=USERINPUT_maxIters)
            traces, iters, I_plot = CollatzConjecture.SVL.Series_RangeConvergeVis(ConvergeFuncManyValues, computeRange, plotSkip=1, titles=['Start Value', 'Convergence Iterations Count', 'Values vs Collatz Convergence Time'], plot=False)

            # Display Outputs
            st.markdown("## Range Iterations")
            st.image(I_plot, "Range Iterations", use_column_width=True)
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()