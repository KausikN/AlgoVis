"""
Stream lit GUI for Sort Algorithms
"""

# Imports
from streamlit_common_utils._common import DictData
from streamlit_common_utils.streamlit_common_ui_setup import *

from .SortingVis import *

# Main Functions
def main(selected="Sort Algorithms", MODES=[], global_override_vars=None, **kwargs):
    # Update global variables
    if global_override_vars: globals().update(global_override_vars)

    # Set Project Modes
    UI_CONFIG = DictData({
        "PROJECT_MODES": MODES
    })

    # Create Sidebar
    build_sidebar_app(UI_CONFIG, globals(), show_home_page=False, sidebar_title="Choose Sort Algorithm")


#############################################################################################################################
# Repo Based Vars
PATHS = {}
DEFAULT_VIDEO_DURATION = 2.0

# Util Vars


# Util Functions


# Main Functions


# UI Functions
def UI_DisplaySortingOutput(array, array_sorted, trace):
    '''
    UI - Display Sorting Output
    '''
    # Title
    st.markdown("## Sort Output")

    colsize = (1, 3)
    
    col1, col2 = st.columns(colsize)
    col1.markdown("Input Array")
    col2.markdown("```python\n" + str([int(x) for x in array]))

    col1, col2 = st.columns(colsize)
    col1.markdown("Sorted Array")
    col2.markdown("```python\n" + str([int(x) for x in array_sorted]))

    col1, col2 = st.columns(colsize)
    col1.markdown("Number of Swaps")
    col2.markdown("```python\n" + str(len(trace)) + " swaps")

    # Display Video
    VideoData = open(PATHS["default"]["save"]["video_converted"], "rb").read()
    st.video(VideoData)

# Repo Based Functions
def sort_algorithms(**kwargs):
    # Title
    st.header("Sort Algorithms")

    # Prereq Loaders

    # Load Inputs
    SORT_FUNCS_NAMES = list(SORT_ALGORITHMS.keys())
    USERINPUT_SortAlgoName = st.selectbox("Select Sort Algorithm", SORT_FUNCS_NAMES)

    USERINPUT_ArraySize = st.slider("Select Array Size", 5, 100, 25, 5)

    # Process Inputs
    if st.button("Visualise"):
        USERINPUT_SortFunc = SORT_ALGORITHMS[USERINPUT_SortAlgoName]

        # Generate Array
        array = GenerateArray_Random(USERINPUT_ArraySize)

        # Visualise Array
        array_sorted, trace = SortVis_PlotGIF(USERINPUT_SortFunc, array, PATHS["default"]["save"]["video_converted"], duration=DEFAULT_VIDEO_DURATION)
        # array_sorted, trace = SortVis_PlotGIF(USERINPUT_SortFunc, array, PATHS["default"]["save"]["video"], duration=DEFAULT_VIDEO_DURATION)
        
        # Display Outputs
        UI_DisplaySortingOutput(array, array_sorted, trace)
    
#############################################################################################################################
# Run Code
if __name__ == "__main__":
    main()