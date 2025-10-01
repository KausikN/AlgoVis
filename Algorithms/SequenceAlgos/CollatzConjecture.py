"""
Algorithm Visualisation for the Collatz Conjecture
Link: https://www.youtube.com/watch?v=5mFpVDpKX70
"""

# Imports
import functools
from .._Libraries import SeriesVisualiseLibrary as SVL

# Main Functions
# Algorithm Functions
def CollatzConjecture_Converge(startVal, max_iters=-1):
    '''
    Collatz Conjecture - Converge using the Collatz Conjecture
    '''
    values = [startVal]
    curVal = startVal
    n_iters = 0
    while(curVal > 1):
        if curVal % 2 == 0:
            curVal = int(round(curVal / 2))
        else:
            curVal = 3*curVal + 1

        values.append(curVal)

        n_iters += 1
        if n_iters > max_iters and max_iters > -1:
            break

    return values

# Main Vars
COLLATZ_FUNCS = {
    "Collatz Conjecture": CollatzConjecture_Converge
}

# Driver Code