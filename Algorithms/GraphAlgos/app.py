"""
Stream lit GUI for Graph Algorithms
"""

# Imports
import json
from streamlit_common_utils._common import DictData
from streamlit_common_utils.streamlit_common_ui_setup import *

from Algorithms.GraphAlgos.BFS import *

# Main Functions
def main(selected="Graph Algorithms", MODES=[], global_override_vars=None, **kwargs):
    # Update global variables
    if global_override_vars: globals().update(global_override_vars)

    # Set Project Modes
    UI_CONFIG = DictData({
        "PROJECT_MODES": MODES
    })

    # Create Sidebar
    build_sidebar_app(UI_CONFIG, globals(), show_home_page=False, sidebar_title="Choose Graph Algorithm")


#############################################################################################################################
# Repo Based Vars
PATHS = {}
DEFAULT_VIDEO_DURATION = 2.0
GRAPH_DEFAULT_PATH_EXAMPLE = "Data/DefaultData/ExampleGraph.json"
GRAPH_LOADTYPES = ["Load JSON", "Generate Random Graph"]

# Util Vars


# Util Functions


# Main Functions


# UI Functions
def UI_GraphLoad():
    '''
    UI - Load Graph
    '''
    
    USERINPUT_GraphLoadType = st.selectbox("Select Graph Load Type", GRAPH_LOADTYPES)

    USERINPUT_AdjMatrix = None

    # Load Image
    if USERINPUT_GraphLoadType == GRAPH_LOADTYPES[0]:
        
        USERINPUT_JSONData = st.file_uploader("Upload JSON", ["json"])
        if USERINPUT_JSONData is None:
            USERINPUT_JSONData = open(GRAPH_DEFAULT_PATH_EXAMPLE, "rb")
        USERINPUT_JSONData = json.load(USERINPUT_JSONData)

        USERINPUT_AdjMatrix = generate_adjacency_matrix_from_json_data(USERINPUT_JSONData)

    # Genrate Random Graph
    elif USERINPUT_GraphLoadType == GRAPH_LOADTYPES[1]:
        col1, col2, col3 = st.columns(3)
        USERINPUT_N = col1.number_input("Number of Vertices", 2, 100, 5, 1)
        USERINPUT_ProbEdge = col2.slider("Probability of Edge", 0.0, 1.0, 0.5, 0.05)
        USERINPUT_WeightRange = col3.slider("Enter Weights Range", -100, 100, (-10, 10), 1)
        USERINPUT_WeightsIntOnly = st.checkbox("Integer Weights Only?")

        USERINPUT_AdjMatrix = generate_adjacency_matrix_random(USERINPUT_N, USERINPUT_ProbEdge, USERINPUT_WeightRange, USERINPUT_WeightsIntOnly)

    # Display Graph
    USERINPUT_Image, NodesPos = PlotGraph_AdjacencyMatrix(USERINPUT_AdjMatrix, show_edge_wt=True)
    st.image(USERINPUT_Image, caption="Input Graph", use_container_width=True)

    return USERINPUT_AdjMatrix, NodesPos

# Repo Based Functions
def bfs(**kwargs):
    # Title
    st.header("BFS: Breadth First Search")

    # Prereq Loaders

    # Load Inputs
    st.markdown("## Data Generation Inputs")
    USERINPUT_AdjMatrix, NodesPos = UI_GraphLoad()

    st.markdown("## BFS Inputs")
    USERINPUT_StartNode = st.number_input("Enter Start Node", 0, USERINPUT_AdjMatrix.shape[0] - 1)

    # Process Inputs
    if st.button("Visualise"):
        # print(USERINPUT_AdjMatrix)
        # Run BFS
        Results = BFS(USERINPUT_AdjMatrix, USERINPUT_StartNode)
        # print(Results)
        # Save Animation
        Animate_BFS(USERINPUT_AdjMatrix, Results, NodesPos, PATHS["default"]["save"]["video_converted"], duration=DEFAULT_VIDEO_DURATION, use_stqdm=True)
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"]) 
    
#############################################################################################################################
# Run Code
if __name__ == "__main__":
    main()