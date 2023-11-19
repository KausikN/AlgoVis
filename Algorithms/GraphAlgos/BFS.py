"""
Breadth First Search Algorithm
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm

from .._Libraries import GraphVis
from .._Libraries import DatasetGenerators
from .._Libraries import VideoUtils

# Main Functions
# Evaluation and Visualization
def Animate_BFS(AdjMatrix, Results, NodesPos, savePath, duration=2.0):
    trace = Results["trace"]

    # Generate Plot Images
    Is = []
    for i in tqdm(range(len(trace))):
        iterData = trace[i]
        visited = iterData["visited"]
        colors = [GraphVis.GetColor(visited[i]) for i in range(len(visited))]
        I_plot, _ = GraphVis.PlotGraph_AdjacencyMatrix(AdjMatrix, colors, title="BFS Trace Iteration " + str(iterData["iter"]), pos=NodesPos, plot=False)
        Is.append(I_plot)

    # Save Video/GIF
    fps = len(Is)/duration
    VideoUtils.SaveFrames2Video(Is, savePath, fps=fps)

# BFS Algorithm
def BFS(AdjMatrix, source=0):
    '''
    Perform BFS on the given Graph starting at the source
    '''

    # Initialize
    AdjMatrix = np.array(AdjMatrix)
    N = AdjMatrix.shape[0]
    visited = np.zeros(N, dtype=float)

    Results = {}
    trace = []
    
    currIter = {"iter": 0, "visited": deepcopy(visited)}
    trace.append(currIter)

    visited[source] = 1.0

    currIter = {"iter": 0, "visited": deepcopy(visited)}
    trace.append(currIter)

    # BFS
    queue = [source]
    while len(queue) > 0:
        # Pop
        u = queue.pop(0)
        # Update
        visited[u] = 1.0
        # Push
        for v in range(AdjMatrix.shape[1]):
            if not (AdjMatrix[u, v] == np.inf) and not (visited[v] == 1.0):
                queue.append(v)
                visited[v] = 0.5
        # Update Trace
        currIter = {"iter": len(trace), "visited": deepcopy(visited)}
        trace.append(currIter)
    
    Results = {}
    Results["source"] = source
    Results["visited"] = visited
    Results["trace"] = trace
    return Results

# Driver Code