"""
Stream lit GUI for Graph Algorithms
"""

# Imports
import os
import cv2
import numpy as np
import streamlit as st
import json
import subprocess
import functools

from Algorithms.GraphAlgos import BFS

# Main Functions
def main_ClusteringAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose Graph Algorithm',
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
GRAPH_DEFAULT_PATH_EXAMPLE = "StreamLitGUI/DefaultData/ExampleGraph.json"
GRAPH_LOADTYPES = ["Load JSON", "Generate Random Graph"]

# Util Vars


# Util Functions


# Main Functions


# UI Functions
def UI_GraphLoad():
    
    USERINPUT_GraphLoadType = st.selectbox("Select Graph Load Type", GRAPH_LOADTYPES)

    USERINPUT_AdjMatrix = None

    # Load Image
    if USERINPUT_GraphLoadType == GRAPH_LOADTYPES[0]:
        
        USERINPUT_JSONData = st.file_uploader("Upload JSON", ['json'])
        if USERINPUT_JSONData is None:
            USERINPUT_JSONData = open(GRAPH_DEFAULT_PATH_EXAMPLE, 'rb')
        USERINPUT_JSONData = json.load(USERINPUT_JSONData)

        USERINPUT_AdjMatrix = BFS.DatasetGenerators.GenerateAdjacencyMatrixFromJSONData(USERINPUT_JSONData)

    # Genrate Random Graph
    elif USERINPUT_GraphLoadType == GRAPH_LOADTYPES[1]:
        col1, col2, col3 = st.columns(3)
        USERINPUT_N = col1.number_input("Number of Vertices", 2, 100, 5, 1)
        USERINPUT_ProbEdge = col2.slider("Probability of Edge", 0.0, 1.0, 0.5, 0.05)
        USERINPUT_WeightRange = col3.slider("Enter Weights Range", -100, 100, (-10, 10), 1)
        USERINPUT_WeightsIntOnly = st.checkbox("Integer Weights Only?")

        USERINPUT_AdjMatrix = BFS.DatasetGenerators.GenerateRandomAdjacencyMatrix(USERINPUT_N, USERINPUT_ProbEdge, USERINPUT_WeightRange, USERINPUT_WeightsIntOnly)

    # Display Graph
    USERINPUT_Image, NodesPos = BFS.GraphVis.PlotGraph_AdjacencyMatrix(USERINPUT_AdjMatrix, show_edge_wt=True, plot=False)
    st.image(USERINPUT_Image, caption="Input Graph", use_column_width=True)

    return USERINPUT_AdjMatrix, NodesPos

# Repo Based Functions
def bfs():
    global DEFAULT_VIDEO_DURATION

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
        Results = BFS.BFS(USERINPUT_AdjMatrix, USERINPUT_StartNode)
        # print(Results)
        # Save Animation
        BFS.Animate_BFS(USERINPUT_AdjMatrix, Results, NodesPos, DEFAULT_SAVEPATH_VIDEO, duration=DEFAULT_VIDEO_DURATION)
        BFS.VideoUtils.FixVideoFile(DEFAULT_SAVEPATH_VIDEO, DEFAULT_SAVEPATH_VIDEO_CONVERTED)
        # Display Animation Video
        st.video(DEFAULT_SAVEPATH_VIDEO_CONVERTED) 
    
#############################################################################################################################
# Driver Code
main_ClusteringAlgos()