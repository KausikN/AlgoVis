"""
Algorithm Visualisation for any Equation
Gravity Link: https://www.youtube.com/watch?v=mezkHBPLZ4A
"""

# Imports
import functools
from turtle import ycor
import numpy as np
from .._Libraries import Plot3DVisualiseLibrary as P3L
from .FunctionsLibrary.TransformFunctions import *

# Main Functions
# Main Equation Functions
def EquationVis_2D_Generic(X, TransformFunc, startPos=0.0, scale=1.0):
    '''
    Equation Vis - Generic 2D Equation Visualization
    '''
    Ys = []
    curState = startPos
    for x in X:
        y = TransformFunc([x, curState]) * scale
        Ys.append(y)
    Ys = np.array(Ys)

    return Ys

def EquationVis_2D_Combined(Ys, combinationStr="{F1}"):
    '''
    Equation Vis - Combine multiple 2D Equations into one using combination string
    '''
    N = Ys.shape[1]
    Ys_combined = []
    for i in range(N):
        varDict = {}
        for j in range(Ys.shape[0]): varDict["F" + str(j+1)] = Ys[j, i]
        y = 0.0
        try:
            y = eval(combinationStr.format(**varDict))
        except:
            pass
        Ys_combined.append(y)
    Ys_combined = np.array(Ys_combined)

    return Ys_combined

# Driver Code