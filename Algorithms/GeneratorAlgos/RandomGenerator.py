"""
PlotGIFLibrary is a library for generation, editing and viewing of GIFs / Videos of Plot Data
"""

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .._Libraries.VideoUtils import *

# Main Params
YData = {}
XData = {}
plotData = {}

# Main Vars
fig = plt.figure()
canvas = FigureCanvasAgg(fig)

# Main Functions
# Random Functions
def RandomFrequencyDistribution_Vis(numRange=(0, 100), nframes=100, title=""):
    '''
    Random Frequency Distribution - Visualise the distribution of random number generator in python by visualising the frequency distribution
    '''
    # Setup Plot
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)

    # Generate Random Numbers
    randVals = np.random.randint(numRange[0], numRange[1]+1, nframes)
    xs = list(range(numRange[0], numRange[1]+1))
    curFreqs = np.zeros(len(xs))

    Is = []
    for r in randVals:
        fig.clear()
        plt.title(title)
        ax = plt.axes()

        curFreqs[xs.index(r)] += 1
        # Plot the data
        plt.bar(xs, curFreqs)

        # Retrieve Image
        canvas.draw()
        buf = canvas.buffer_rgba()
        I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)
        Is.append(I_plot)

    plt.close(fig)
    return Is

def Random2DPointsGenerator_Vis(valuesBound=[(0, 100), (0, 100)], nframes=100, title=""):
    '''
    Random Generator - 2D - Visualise generation of random 2D points within given bounds
    '''
    # Setup Plot
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)

    # Generate Random Points
    randPointsX = np.random.uniform(valuesBound[0][0], valuesBound[0][1], nframes)
    randPointsY = np.random.uniform(valuesBound[1][0], valuesBound[1][1], nframes)
    randPoints = np.dstack((randPointsX, randPointsY))[0]

    Is = []
    for i in range(randPoints.shape[0]):
        fig.clear()
        plt.title(title)
        ax = plt.axes()
        ax.set_xlim(valuesBound[0][0], valuesBound[0][1])
        ax.set_ylim(valuesBound[1][0], valuesBound[1][1])

        # Plot the data
        ax.scatter(randPoints[:i+1][:, 0], randPoints[:i+1][:, 1])

        # Retrieve Image
        canvas.draw()
        buf = canvas.buffer_rgba()
        I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)
        Is.append(I_plot)

    plt.close(fig)
    return Is

def Random3DPointsGenerator_Vis(valuesBound=[(0, 100), (0, 100), (0, 100)], nframes=100, title=""):
    '''
    Random Generator - 3D - Visualise generation of random 3D points within given bounds
    '''
    # Setup Plot
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)

    # Generate Random Points
    randPointsX = np.random.uniform(valuesBound[0][0], valuesBound[0][1], nframes)
    randPointsY = np.random.uniform(valuesBound[1][0], valuesBound[1][1], nframes)
    randPointsZ = np.random.uniform(valuesBound[2][0], valuesBound[2][1], nframes)
    randPoints = np.dstack((randPointsX, randPointsY, randPointsZ))[0]

    Is = []
    for i in range(randPoints.shape[0]):
        fig.clear()
        plt.title(title)
        ax = plt.axes(projection="3d")
        ax.set_xlim(valuesBound[0][0], valuesBound[0][1])
        ax.set_ylim(valuesBound[1][0], valuesBound[1][1])

        # Plot the data
        ax.scatter3D(randPoints[:i+1][:, 0], randPoints[:i+1][:, 1], randPoints[:i+1][:, 2])

        # Retrieve Image
        canvas.draw()
        buf = canvas.buffer_rgba()
        I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)
        Is.append(I_plot)

    plt.close(fig)
    return Is
    

# Run Code