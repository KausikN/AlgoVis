"""
Library Functions for 3D Plot Visualisation
"""

# Imports
import os
import numpy as np
from tqdm import tqdm
from stqdm import stqdm
from matplotlib import animation
from matplotlib import pyplot as plt

from streamlit_common_utils.dataset import *

# Main Variables
Lines = []
Pts = []
fig = None
ax = None
x_t = []
speedUpFactor = 2
rotationSpeed = 3
initRot = 30

# Main Functions
# Visualisation Functions
# initialization function: plot the background of each frame
def InitAnimation():
    '''
    Initialize the animation
    '''
    global Lines, Pts, x_t, fig, ax
    for line, pt in zip(Lines, Pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return Lines + Pts

# animation function.  This will be called sequentially with the frame number
def UpdateAnimation(i):
    '''
    Update the animation by one frame
    '''
    global Lines, Pts, x_t, fig, ax, speedUpFactor, rotationSpeed
    print(i, "done", end="\r")
    # we"ll step two time-steps per frame.  This leads to nice results.
    i = (speedUpFactor * i) % x_t.shape[1]

    for line, pt, xi in zip(Lines, Pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    ax.view_init(initRot, i*rotationSpeed)
    fig.canvas.draw()

    return Lines + Pts

def AnimateEffect(EffectFunc, N_trajectories, GeneratorFunc, timeInterval=[0, 4], plotLims=[(-25, 25), (-35, 35), (5, 55)], frames=500, frame_interval=30, plotData=True, saveData={"save": False}, use_stqdm=False):
    '''
    Animate Effect - Animate the effect of a function on a set of points
    '''
    global Lines, Pts, x_t, fig, ax, speedUpFactor
    TQDM = stqdm if use_stqdm else tqdm

    # Choose random starting points, uniformly distributed from -15 to 15
    startPoints = GeneratorFunc(N_trajectories)
    N_trajectories = startPoints.shape[0]

    # Get Plot Points
    time = np.linspace(timeInterval[0], timeInterval[1], frames*speedUpFactor)
    x_t = np.asarray([EffectFunc(sP, time) for sP in TQDM(startPoints)])

    # Set up figure & 3D axis for animation
    fig = plt.figure(figsize=saveData["figSize"])
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.axis("off")

    # choose a different color for each trajectory
    colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

    # Set up lines and points
    Lines = sum([ax.plot([], [], [], "-", c=c) for c in colors], [])
    Pts = sum([ax.plot([], [], [], "o", c=c) for c in colors], [])

    # Prepare the axes limits
    ax.set_xlim(plotLims[0])
    ax.set_ylim(plotLims[1])
    ax.set_zlim(plotLims[2])

    # Set point-of-view: specified by (altitude degrees, azimuth degrees)
    ax.view_init(initRot, 0)

    # Animate
    InitAnim = InitAnimation
    UpdateAnim = UpdateAnimation
    anim = animation.FuncAnimation(fig, UpdateAnim, init_func=InitAnim, frames=frames, interval=frame_interval, blit=True)

    # Save as mp4. This requires mplayer or ffmpeg to be installed
    if saveData["save"]:
        if os.path.splitext(saveData["path"])[-1] == ".gif":
            writer = animation.PillowWriter(fps=saveData["fps"])
            anim.save(saveData["path"], writer=writer, )
        else:
            anim.save(saveData["path"], fps=saveData["fps"], extra_args=["-vcodec", "libx264"])

    if plotData:
        plt.show()


def AnimateEffect_Generic(EffectFunc, Points, Colors, timeInterval=[0, 4], plotLims=[(-25, 25), (-35, 35), (5, 55)], frames=500, frame_interval=30, plotData=True, saveData={"save": False}, use_stqdm=False):
    '''
    Animate Effect - Generically animate the effect of a function on a set of points
    '''
    global Lines, Pts, x_t, fig, ax, speedUpFactor
    TQDM = stqdm if use_stqdm else tqdm

    # Choose random starting points, uniformly distributed from -15 to 15
    startPoints = np.array(Points)
    N_trajectories = startPoints.shape[0]

    # Get Plot Points
    time = np.linspace(timeInterval[0], timeInterval[1], frames*speedUpFactor)
    x_t = np.asarray([EffectFunc(sP, time) for sP in TQDM(startPoints)])

    # Set up figure & 3D axis for animation
    fig = plt.figure(figsize=saveData["figSize"])
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.axis("off")

    # choose a different color for each trajectory
    colors = np.array(Colors)

    # Set up lines and points
    Lines = sum([ax.plot([], [], [], "-", c=c) for c in colors], [])
    Pts = sum([ax.plot([], [], [], "o", c=c) for c in colors], [])

    # Prepare the axes limits
    ax.set_xlim(plotLims[0])
    ax.set_ylim(plotLims[1])
    ax.set_zlim(plotLims[2])

    # Set point-of-view: specified by (altitude degrees, azimuth degrees)
    ax.view_init(initRot, 0)

    # Animate
    InitAnim = InitAnimation
    UpdateAnim = UpdateAnimation
    anim = animation.FuncAnimation(fig, UpdateAnim, init_func=InitAnim, frames=frames, interval=frame_interval, blit=True)

    # Save as mp4. This requires mplayer or ffmpeg to be installed
    if saveData["save"]:
        if os.path.splitext(saveData["path"])[-1] == ".gif":
            writer = animation.PillowWriter(fps=saveData["fps"])
            anim.save(saveData["path"], writer=writer, )
        else:
            anim.save(saveData["path"], fps=saveData["fps"], extra_args=["-vcodec", "libx264"])

    if plotData:
        plt.show()