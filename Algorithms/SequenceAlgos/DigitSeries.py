'''
Digit based Series generation and visualisation
'''

# Imports
import functools
import numpy as np
from .._Libraries import SeriesVisualiseLibrary as SVL

# Main Functions
# Converge Functions
def DigitSeries_Sum_Converge(startVal, max_iters=-1):
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

def DigitSeries_Multiply_Converge(startVal, max_iters=-1):
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
    "Digit Sum Series": DigitSeries_Sum_Converge,
    "Digit Multiply Series": DigitSeries_Multiply_Converge
}

# Driver Code