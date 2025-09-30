"""
Linear Regression
"""

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from .._Libraries import DatasetGenerators

# Main Vars
fig = plt.figure()
canvas = FigureCanvasAgg(fig)

# Main Functions
def PolynomialRegression(x, y, degree):
    '''
    Polynomial Regression using Normal Equation Method
    '''
    # In Polynomial Regression we have,
    # y = b0 + b1*x + b2*x^2 + ... bn*x^n

    # Transform X
    X_transformed = []
    for x_val in x:
        x_poly = [1]
        for p in range(1, degree+1):
            x_poly.append(x_val**p)
        X_transformed.append(x_poly)
    X_transformed = np.array(X_transformed)

    # Calculate Regression Parameters
    phi = X_transformed
    phiTphi = np.matmul(phi.T, phi)
    phiTphi_inv = np.linalg.inv(phiTphi)
    phiTy = np.matmul(phi.T, y)
    b = np.dot(phiTphi_inv, phiTy)

    return b

def LinearRegression(x, y):
    '''
    Linear Regression using Least Squares Method
    '''
    # In Linear Regression we have,
    # y = b0 + b1*x
    # where,
    # b0 = y_mean - b1*x_mean
    # b1 = covariance_xy/variance_xx

    N = x.shape[0]
 
    # Mean of X and Y
    x_mean = np.mean(x)
    y_mean = np.mean(y)
 
    # Variance and Covariance
    covariance_xy = np.sum(x * y) - N * y_mean * x_mean
    variance_xx = np.sum(x * x) - N * x_mean * x_mean
 
    # Calculate Regression parameters
    b_1 = covariance_xy / variance_xx
    b_0 = y_mean - b_1 * x_mean
 
    return (b_0, b_1)

# Predict and Error Functions
def Predict(b, x):
    '''
    Predict y values for given x using coefficients b
    '''
    y_pred = np.array([b[0]] * len(x))
    for i in range(1, len(b)):
        y_pred = y_pred + (b[i] * (x ** i))
    return y_pred

def Error_SumSquares(y, y_pred):
    '''
    Calculate Sum of Squares Error between actual and predicted y values
    '''
    y = np.array(y)
    y_pred = np.array(y_pred)
    return np.sum((y - y_pred) ** 2)

def GetErrors(x, y, degrees_coeffs):
    '''
    Get Errors for multiple polynomial degrees
    '''
    y_preds = []
    for i in range(len(degrees_coeffs)):
        y_preds.append(Predict(degrees_coeffs[i], x))
    errors = []
    for i in range(len(degrees_coeffs)):
        errors.append(Error_SumSquares(y, y_preds[i]))
    return errors

# Display Functions
def DisplayPolynomial(coeffs):
    '''
    Display Polynomial as String
    '''
    polyStr = f"y = {coeffs[0]}"
    for i in range(1, len(coeffs)):
        polyStr += f" + {coeffs[i]}*x^{i}"

    return polyStr

# Plot Functions
def PlotRegressionCurves(x, y, bs, degrees, title="", curve_pts=1000):
    '''
    Plot Regression Curves for multiple polynomial degrees
    '''
    # Setup Plot
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)

    # Order the Points
    xy = sorted(zip(x, y))
    x = np.array([i[0] for i in xy])
    y = np.array([i[1] for i in xy])

    # Plot Actual Points
    plt.scatter(x, y, label="Points")
 
    x = np.linspace(np.min(x), np.max(x), curve_pts)
    for i in range(len(bs)):
        b = bs[i]
        deg = degrees[i]
        # Predict
        y_pred = Predict(b, x)
        # Plot Regression Line
        plt.plot(x, y_pred, label="Degree " + str(deg))

    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    # plt.show()

    # Retrieve Image
    canvas.draw()
    buf = canvas.buffer_rgba()
    I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    # plt.close(fig)
    return I_plot, fig

def PlotPredictions(x, y, y_pred, degree, title=""):
    '''
    Plot Predictions for given polynomial degree
    '''
    # Setup Plot
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)

    # Order the Points
    xy = sorted(zip(x, y, y_pred))
    x = np.array([i[0] for i in xy])
    y = np.array([i[1] for i in xy])
    y_pred = np.array([i[2] for i in xy])

    # Plot Actual Points
    plt.scatter(x, y, label="Actual Points")
    # Plot Regression Line
    plt.scatter(x, y_pred, label="Predicted Points for Degree " + str(degree))

    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    # plt.show()

    # Retrieve Image
    canvas.draw()
    buf = canvas.buffer_rgba()
    I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    # plt.close(fig)
    return I_plot, fig

def PlotErrors(errors, degrees, title=""):
    '''
    Plot Errors for multiple polynomial degrees
    '''
    # Setup Plot
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)

    plt.plot(degrees, errors)

    plt.legend()
    plt.title(title)
    plt.xlabel("Degrees")
    plt.ylabel("Error")
    # plt.show()

    # Retrieve Image
    canvas.draw()
    buf = canvas.buffer_rgba()
    I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)

    # plt.close(fig)
    return I_plot, fig

# Driver Code