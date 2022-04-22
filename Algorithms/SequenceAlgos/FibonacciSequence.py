'''
Algorithm Visualisation for Fibonacci and related series
Link: https://www.youtube.com/watch?v=SjSHVDfXHQ4
'''

# Imports
import functools
import numpy as np
from .._Libraries import SeriesVisualiseLibrary as SVL

# Main Functions
# Algorithm Functions
def Fibonacci_Standard(iters, startVals=[1, 1]):
    values = [startVals[0], startVals[1]]
    curVals = [startVals[0], startVals[1]]
    curIter = 0
    while(curIter < iters):
        curVals = [curVals[1], curVals[0] + curVals[1]]
        values.append(curVals[1])
        curIter += 1

    return values

def Fibonacci_GenericLength(iters, startVals=[1, 1]):
    values = list(startVals)
    curVals = list(startVals)
    curIter = 0
    while(curIter < iters):
        curVals = curVals[1:] + [(np.sum(np.array(curVals)))]
        values.append(curVals[-1])
        curIter += 1

    return values

def Fibonacci_GenericFunc(iters, NextFunc, startVals=[1, 1]):
    values = list(startVals)
    curVals = list(startVals)
    curIter = 0
    while(curIter < iters or iters == -1):
        curVals, newVal, stop = NextFunc(curVals, curIter, iters)
        values.append(newVal)
        curIter += 1
        if stop:
            break

    return values

# Generic Fibonacci Functions
def FibonacciGenericFunc_OddAdd(curVals, curIter, iters):
    curVals = curVals[1:] + [(np.sum(np.array(curVals)[1::2]))]
    newVal = curVals[-1]
    return curVals, newVal, False

def FibonacciGenericFunc_EvenAdd(curVals, curIter, iters):
    curVals = curVals[1:] + [(np.sum(np.array(curVals)[::2]))]
    newVal = curVals[-1]
    return curVals, newVal, False

def FibonacciGenericFunc_InverseAdd(curVals, curIter, iters):
    curVals = curVals[1:] + [(np.sum(1/np.array(curVals)))]
    newVal = curVals[-1]
    return curVals, newVal, False

def FibonacciGenericFunc_ReverseGenericLength(curVals, curIter, iters, positiveOnly=False):
    curVals = curVals[1:] + [curVals[0] - (np.sum(np.array(curVals[1:])))]
    newVal = curVals[-1]
    return curVals, newVal, (newVal <= 0) and (positiveOnly)

# Main Vars
FIBONACCISERIES_FUNCS = {
    "Standard": Fibonacci_Standard,
    "Generic Length": Fibonacci_GenericLength,
    "Add Odd Elements": functools.partial(Fibonacci_GenericFunc, NextFunc=FibonacciGenericFunc_OddAdd),
    "Add Even Elements": functools.partial(Fibonacci_GenericFunc, NextFunc=FibonacciGenericFunc_EvenAdd),
    "Add Reciprocals": functools.partial(Fibonacci_GenericFunc, NextFunc=FibonacciGenericFunc_InverseAdd),
    "Subtract from first Element": functools.partial(Fibonacci_GenericFunc, 
        NextFunc=functools.partial(FibonacciGenericFunc_ReverseGenericLength, positiveOnly=True)
    )
}

# Driver Code