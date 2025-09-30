"""
Algorithm Visualisation for Recaman Sequence
Link: https://www.youtube.com/watch?v=FGC5TdIiT9U
"""

# Imports
import functools
from .._Libraries import SeriesVisualiseLibrary as SVL

# Main Functions
# Algorithm Functions
def Recaman_Standard(startVal, iters=10, minFill=-1):
    '''
    Standard Recaman Sequence
    '''
    values = [startVal]
    curVal = startVal
    curStep = 1
    minAllVisited = 0
    visitedVals = []

    curIter = 0
    while(curIter < iters or (minFill > 0 and minAllVisited < minFill)):
        newVal = curVal
        leftVal = curVal - curStep
        rightVal = curVal + curStep
        if leftVal <= minAllVisited:
            # If Left Path Blocked check Right
            if rightVal in visitedVals:
                # Both Ways Blocked - GO RIGHT BY DEFAULT
                newVal = rightVal
            else:
                # Right available
                newVal = rightVal
        else:
            # If Left Path not blocked, check if not in visited
            if leftVal in visitedVals:
                # Left Path visited, Check Right
                if rightVal in visitedVals:
                    # Both Ways Blocked - GO RIGHT BY DEFAULT
                    newVal = rightVal
                else:
                    # Right available
                    newVal = rightVal
            else:
                # Left Available
                newVal = leftVal

        
        visitedVals.append(newVal)
        # Prune visitedVals and update minAllVisited
        minI = 1
        while(True):
            checkVal = minAllVisited + minI
            if checkVal in visitedVals:
                minI += 1
                minAllVisited += 1
                visitedVals.remove(checkVal)
                # print(minAllVisited)
            else:
                break

        # Update other vars
        curVal = newVal
        values.append(curVal)
        curStep += 1

        curIter += 1

    return values

# Main Vars
RECAMAN_FUNCS = {
    "Standard": Recaman_Standard
}

# Driver Code