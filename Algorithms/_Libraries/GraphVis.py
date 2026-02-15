"""
Graph Visualiser
"""

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

import networkx as nx

from streamlit_common_utils.color import *
from streamlit_common_utils.graph import *
from streamlit_common_utils.plot import *

# Main Vars
fig = plt.figure()
canvas = FigureCanvasAgg(fig)

# Main Functions
# Plot Graph Functions
def PlotGraph_AdjacencyMatrix(Adj, colors="#1f78b4", show_edge_wt=False, title="", pos=None):
    '''
    Plot Graph - Plots the adjacency matrix Graph using NetworkX and Matplotlib
    '''
    return plot_networkx_graph(
        generate_networkx_graph_from_adjacency_matrix(Adj), 
        colors=colors, show_edge_wt=show_edge_wt, title=title, pos=pos
    )

# Run Code
# Params

# Params

# RunCode