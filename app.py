"""
Stream lit GUI for hosting {FEATUREDATA_PROJECT_NAME}
"""

# Imports
import os
import streamlit as st
import json
import subprocess

import SortingVis

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
DEFAULT_SAVEPATH_VIDEO = "StreamLitGUI/DefaultData/Video.avi"
DEFAULT_SAVEPATH_VIDEO_CONVERTED = "StreamLitGUI/DefaultData/Video_Converted.mp4"
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
    
    col1, col2 = st.beta_columns(colsize)
    col1.markdown("Input Array")
    col2.markdown("```python\n" + str(array))

    col1, col2 = st.beta_columns(colsize)
    col1.markdown("Sorted Array")
    col2.markdown("```python\n" + str(array_sorted))

    col1, col2 = st.beta_columns(colsize)
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

    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()