"""
Stream lit GUI for Generator Algorithms
"""

# Imports
from streamlit_common_utils._common import DictData
from streamlit_common_utils.streamlit_common_ui_setup import *

from .RandomGenerator import *

# Main Functions
def main(selected="Generator Algorithms", MODES=[], global_override_vars=None, **kwargs):
    # Update global variables
    if global_override_vars: globals().update(global_override_vars)

    # Set Project Modes
    UI_CONFIG = DictData({
        "PROJECT_MODES": MODES
    })

    # Create Sidebar
    build_sidebar_app(UI_CONFIG, globals(), show_home_page=False, sidebar_title="Choose Generator Algorithm")


#############################################################################################################################
# Repo Based Vars
PATHS = {}
DEFAULT_VIDEO_DURATION = 2.0

# Util Vars


# Util Functions


# Main Functions


# UI Functions
def UI_RandomFrequencyDistribution():
    '''
    UI - Random Frequency Distribution
    '''
    USERINPUT_numRange = st.slider("Select Random Value Range", 1, 100, (1, 5), 1)
    USERINPUT_nframes = st.number_input("Select Number of Values to Generate", 1, 500, 10, 1)
    USERINPUT_saveFPS = USERINPUT_nframes / DEFAULT_VIDEO_DURATION

    if st.button("Generate"):
        # Process Inputs
        Is = RandomFrequencyDistribution_Vis(USERINPUT_numRange, USERINPUT_nframes, "Random Frequency Distribution")

        # Display Outputs
        st.markdown("## Generated Random Frequency Distribution")
        save_images_as_video_moviepy(Is, PATHS["default"]["save"]["video_converted"], USERINPUT_saveFPS)
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"])

def UI_Random2DPoints():
    '''
    UI - Random 2D Points
    '''
    col1, col2 = st.columns(2)
    USERINPUT_pointXBounds = col1.slider("Select X Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_pointYBounds = col2.slider("Select Y Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_nframes = st.number_input("Select Number of Points to Generate", 1, 500, 10, 1)
    USERINPUT_saveFPS = USERINPUT_nframes / DEFAULT_VIDEO_DURATION

    if st.button("Generate"):
        # Process Inputs
        Is = Random2DPointsGenerator_Vis([USERINPUT_pointXBounds, USERINPUT_pointYBounds], USERINPUT_nframes, "Random 2D Points")

        # Display Outputs
        st.markdown("## Generated Random 2D Points")
        save_images_as_video_moviepy(Is, PATHS["default"]["save"]["video_converted"], USERINPUT_saveFPS)
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"])

def UI_Random3DPoints():
    '''
    UI - Random 3D Points
    '''
    col1, col2, col3 = st.columns(3)
    USERINPUT_pointXBounds = col1.slider("Select X Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_pointYBounds = col2.slider("Select Y Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_pointZBounds = col3.slider("Select Z Values Bound", 1, 100, (1, 5), 1)
    USERINPUT_nframes = st.number_input("Select Number of Points to Generate", 1, 500, 10, 1)
    USERINPUT_saveFPS = USERINPUT_nframes / DEFAULT_VIDEO_DURATION

    if st.button("Generate"):
        # Process Inputs
        Is = Random3DPointsGenerator_Vis([USERINPUT_pointXBounds, USERINPUT_pointYBounds, USERINPUT_pointZBounds], USERINPUT_nframes, "Random 3D Points")

        # Display Outputs
        st.markdown("## Generated Random 3D Points")
        save_images_as_video_moviepy(Is, PATHS["default"]["save"]["video_converted"], USERINPUT_saveFPS)
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"])

RANDOMGENERATOR_VISUALISAITON_MAP = {
    "Random Frequency Distribution": UI_RandomFrequencyDistribution,
    "Random 2D Points": UI_Random2DPoints,
    "Random 3D Points": UI_Random3DPoints
}

# Repo Based Functions
def random_generators(**kwargs):
    # Title
    st.header("Random Generators")

    # Load Inputs
    USERINPUT_VisChoice = st.selectbox("Select Visualization Type", list(RANDOMGENERATOR_VISUALISAITON_MAP.keys()))

    # Process Inputs
    RANDOMGENERATOR_VISUALISAITON_MAP[USERINPUT_VisChoice]()
    
#############################################################################################################################
# Run Code
if __name__ == "__main__":
    main()