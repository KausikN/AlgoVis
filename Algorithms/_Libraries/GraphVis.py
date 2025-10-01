"""
Graph Visualiser
"""

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

import networkx as nx

# Main Vars
fig = plt.figure()
canvas = FigureCanvasAgg(fig)

# Main Functions
# Utils Functions
def GetColor(i, n=1.0, cmap="gist_gray"):
    '''
    Gets the color for a node in a graph
    '''
    cmap = plt.get_cmap(cmap)
    return cmap(1.0 * (i/n))

def GenerateGraph_AdjacencyMatrix(Adj):
    '''
    Generate Graph - Generates the NetworkX Graph Object from adjacency matrix
    '''
    # Init Graph
    G = nx.Graph()

    # Add Nodes
    for i in range(Adj.shape[0]):
        G.add_node(i)

    # Add Edges
    for i in range(Adj.shape[0]):
        for j in range(Adj.shape[1]):
            if not (Adj[i, j] == np.inf):
                G.add_edge(i, j, weight=Adj[i, j])

    return G

# Plot Graph Functions
def PlotGraph_AdjacencyMatrix(Adj, colors="#1f78b4", show_edge_wt=False, title="", pos=None, plot=False):
    '''
    Plot Graph - Plots the adjacency matrix Graph
    '''
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)
    fig.clear()

    # Init Plot
    ax = plt.axes()

    # Generate Graph Object
    G = GenerateGraph_AdjacencyMatrix(Adj)
    
    # Plot Graph
    if pos is None:
        # pos = nx.spring_layout(G)
        pos = nx.circular_layout(G)
        # pos = nx.multipartite_layout(G)
        # pos = nx.spectral_layout(G)
        # pos = nx.shell_layout(G)
        # pos = nx.planar_layout(G)
        # pos = nx.nx_agraph.graphviz_layout(G)

    nx.draw_networkx(G, pos, ax=ax, with_labels=True, node_color=colors, font_color=(0.3, 1.0, 0.3))

    if show_edge_wt:
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, font_size=7, edge_labels=labels, ax=ax)

    if plot:
        plt.show()
    plt.title(title)
    ax.set_facecolor((0.8, 0.6, 0.6))

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)
    plt.close(fig)

    return I_plot, pos

# Run Code
# Params

# Params

# RunCode