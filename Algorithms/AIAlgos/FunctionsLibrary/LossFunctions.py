'''
Loss Functions
'''

# Imports
import numpy as np

# Main Functions
# Loss Functions
def mean_squared_error(y, t):
    return 0.5 * np.sum((y-t)**2, axis=-1)

def binary_cross_entropy_error(y, t):
    return -np.sum(t * np.log(y + (t == 0)) + (1-t) * (1-np.log(y + ((1-t) == 0))), axis=-1)

def categorical_cross_entropy_error(y, t):
    return -np.sum(t * np.log(y + (t == 0)), axis=-1)

# Derivatives Functions
def mean_squared_error_deriv(y, t):
    return y - t

def binary_cross_entropy_error_deriv(y, t):
    return (-t / y) + ((1-t) / (1-y))

def categorical_cross_entropy_error_deriv(y, t):
    return -t / y

# Main Vars
LOSS_FUNCTIONS = {
    "mean_squared_error": {
        "func": mean_squared_error,
        "deriv": mean_squared_error_deriv
    },
    "binary_cross_entropy_error": {
        "func": binary_cross_entropy_error,
        "deriv": binary_cross_entropy_error_deriv
    },
    "categorical_cross_entropy_error": {
        "func": categorical_cross_entropy_error,
        "deriv": categorical_cross_entropy_error_deriv
    }
}