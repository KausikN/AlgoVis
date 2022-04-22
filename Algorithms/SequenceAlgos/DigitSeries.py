'''
Digit based Series generation and visualisation
'''

# Imports
import functools
import numpy as np
from .._Libraries import SeriesVisualiseLibrary as SVL

# Main Functions
# Converge Functions
def DigitSumSeries_Converge(startVal, max_iters=-1):
    values = [np.abs(startVal)]
    sign = np.sign(startVal)
    curVal = np.abs(startVal)
    n_iters = 0
    while(len(str(curVal)) > 1):
        curVal = np.sum(np.array(list(str(curVal))).astype(int))

        values.append(curVal)

        n_iters += 1
        if n_iters > max_iters and max_iters > -1:
            break

    values = list(np.array(values) * sign)

    return values

def DigitMultiplySeries_Converge(startVal, max_iters=-1):
    values = [np.abs(startVal)]
    sign = np.sign(startVal)
    curVal = np.abs(startVal)
    n_iters = 0
    while(len(str(curVal)) > 1):
        newCurVal = 1
        for v in np.array(list(str(curVal))).astype(int):
            newCurVal *= v
        curVal = newCurVal

        values.append(curVal)

        n_iters += 1
        if n_iters > max_iters and max_iters > -1:
            break

    values = list(np.array(values) * sign)

    return values

# Main Vars
DIGITSERIES_FUNCS = {
    "Digit Sum Series": DigitSumSeries_Converge,
    "Digit Multiply Series": DigitMultiplySeries_Converge
}

# Driver Code