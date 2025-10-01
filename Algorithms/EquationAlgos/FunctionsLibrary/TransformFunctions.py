"""
Transform Functions
"""

# Imports
import math

# Main Functions
def TransformFunc_None(state, **params):
    '''
    Transform Func - No Transformation
    '''
    return 0

def TransformFunc_SinCos(state, coeff=[1, 1], freq=[1, 1], **params):
    '''
    Transform Func - Sin-Cos Transformation
    '''
    x = state[0]
    sinPart = math.sin(x * freq[0]) * coeff[0]
    cosPart = math.cos(x * freq[1]) * coeff[1]
    return sinPart + cosPart

def TransformFunc_Linear(state, coeffs=(0.0, 1.0), **params):
    '''
    Transform Func - Linear Transformation
    '''
    x = state[0]
    return coeffs[0] + (x * coeffs[1])

# Main Vars
TRANSFORM_FUNCS = {
    "None": TransformFunc_None,
    "SinCos": TransformFunc_SinCos,
    "Linear": TransformFunc_Linear
}