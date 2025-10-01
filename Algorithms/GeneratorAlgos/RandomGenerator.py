"""
PlotGIFLibrary is a library for generation, editing and viewing of GIFs / Videos of Plot Data
"""

# Imports
import cv2
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from .._Libraries import PlotAnimateLibrary as PAL
from .._Libraries import VideoUtils

# Main Params
YData = {}
XData = {}
plotData = {}

# Main Vars
fig = plt.figure()
canvas = FigureCanvasAgg(fig)

# Main Functions
# OLD Functions
# Random Generator Vis - Visualise the distribution of random number generator in python by visualising the frequency distribution
def RandomGenerator_Vis_OLD(numRange=(0, 100), frameLim=(0, 100), nframes=100, show=True):
    '''
    Random Generator - Visualise the distribution of random number generator in python by visualising the frequency distribution
    '''
    global XData
    global YData

    XData["lim"] = numRange
    YData["lim"] = (0, 1)
    frames = np.linspace(frameLim[0], frameLim[1], nframes)

    RandomGenerator_CreatePlotFigure()
    YData["maxFreq"] = max(YData["data"])

    return PAL.CreatePlotGIF(plotData["fig"], RandomGenerator_PlotUpdate, RandomGenerator_PlotInit, frames, show)

def RandomGenerator_CreatePlotFigure():
    '''
    Random Generator - Create Plot Figure for Random Generator Visualization
    '''
    global plotData
    global XData
    global YData

    fig, ax = plt.subplots()
    XData["data"] = range(XData["lim"][0], XData["lim"][1] + 1)
    YData["data"] = [0]*(XData["lim"][1] - XData["lim"][0] + 1)
    rects = plt.bar(XData["data"], YData["data"])
    plotData["plotVar"] = rects
    plotData["ax"] = ax
    plotData["fig"] = fig

def RandomGenerator_PlotInit():
    '''
    Random Generator - Initialize Plot for Random Generator Visualization
    '''
    global XData
    global YData
    global plotData
    plotData["ax"].set_xlim(XData["lim"][0], XData["lim"][1])
    plotData["ax"].set_ylim(YData["lim"][0], YData["lim"][1])

def RandomGenerator_PlotUpdate(i):
    '''
    Random Generator - Update Plot for Random Generator Visualization
    '''
    global XData
    global YData
    global plotData
    newVal = random.randint(XData["lim"][0], XData["lim"][1])
    newVal_Index = XData["data"].index(newVal)
    YData["data"][newVal_Index] += 1
    if YData["data"][newVal_Index] > YData["maxFreq"]:
        YData["maxFreq"] = YData["data"][newVal_Index]
        YData["lim"] = (YData["lim"][0], YData["maxFreq"] + 1)
        plotData["ax"].set_ylim(YData["lim"][0], YData["lim"][1])
    plotData["plotVar"][newVal_Index].set_height(YData["data"][newVal_Index])

# New Functions
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
    

# Driver Code