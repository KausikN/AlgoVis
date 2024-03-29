"""
Data Generators
"""

# Imports
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from sklearn.datasets import make_blobs

# Main Vars
fig = plt.figure()
canvas = FigureCanvasAgg(fig)

# Main Functions
# Plot Functions
def PlotLabelledData(Dataset, title="", plot=False):
    '''
    Plots the data with labels.
    '''
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)
    fig.clear()

    X = Dataset["points"]
    labels = Dataset["labels"]
    unique_labels = Dataset["unique_labels"]
    centers = np.array([])
    if "centers" in Dataset.keys():
        centers = Dataset["centers"]

    # Init Plot
    ax = None
    # If 3D
    if Dataset["dim"] >= 3:
        ax = plt.axes(projection="3d")
    else:
        ax = plt.axes()

    # Plot the data
    for ul in unique_labels:
        X_ul = X[labels == ul]

        if Dataset["dim"] >= 3:
            ax.scatter3D(X_ul[:, 0], X_ul[:, 1], X_ul[:, 2], label=ul)
        elif Dataset["dim"] == 2:
            ax.scatter(X_ul[:, 0], X_ul[:, 1], label=ul)
        elif Dataset["dim"] == 1:
            ax.scatter(X_ul[:, 0], np.zeros(X_ul.shape), label=ul)

    # Plot Centers
    if centers.shape[0] > 0:
        centersParams = {"marker": "x", "label": "Centers", "s": 50, "c": "black"}
        if Dataset["dim"] >= 3:
            ax.scatter3D(centers[:, 0], centers[:, 1], centers[:, 2], **centersParams)
        elif Dataset["dim"] == 2:
            ax.scatter(centers[:, 0], centers[:, 1], **centersParams)
        elif Dataset["dim"] == 1:
            ax.scatter(centers[:, 0], np.zeros(centers.shape), **centersParams)

    plt.legend()
    plt.title(title)

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)
    
    if plot:
        plt.show()
    plt.close(fig)

    return I_plot

def PlotUnlabelledData(Dataset, title="", lines=True, plot=False):
    '''
    Plots the datapoints.
    '''
    global fig, canvas
    fig = plt.figure()
    canvas = FigureCanvasAgg(fig)
    fig.clear()

    X = Dataset["points"]
    centers = np.array([])
    if "centers" in Dataset.keys():
        centers = Dataset["centers"]

    # Init Plot
    ax = None
    # If 3D
    if Dataset["dim"] >= 3:
        ax = plt.axes(projection="3d")
    else:
        ax = plt.axes()

    # Plot the data
    if Dataset["dim"] >= 3:
        if not lines:
            ax.scatter3D(X[:, 0], X[:, 1], X[:, 2])
        else:
            ax.plot3D(X[:, 0], X[:, 1], X[:, 2])
    elif Dataset["dim"] == 2:
        if not lines:
            ax.scatter(X[:, 0], X[:, 1])
        else:
            ax.plot(X[:, 0], X[:, 1])
    elif Dataset["dim"] == 1:
        if not lines:
            ax.scatter(X[:, 0], np.zeros(X.shape))
        else:
            ax.plot(X[:, 0], np.zeros(X.shape))

    # Plot Centers
    if centers.shape[0] > 0:
        centersParams = {"marker": "x", "label": "Centers", "s": 50, "c": "black"}
        if Dataset["dim"] >= 3:
            ax.scatter3D(centers[:, 0], centers[:, 1], centers[:, 2], **centersParams)
        elif Dataset["dim"] == 2:
            ax.scatter(centers[:, 0], centers[:, 1], **centersParams)
        elif Dataset["dim"] == 1:
            ax.scatter(centers[:, 0], np.zeros(centers.shape), **centersParams)

    # plt.legend()
    plt.title(title)

    canvas.draw()
    buf = canvas.buffer_rgba()
    I_plot = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)
    
    if plot:
        plt.show()
    plt.close(fig)

    return I_plot

# Generate Functions
# Points Datasets
def GenerateRandomBlobs(N, dim, centers, plot=False):
    '''
    Generates a random dataset of 2D points.
    '''
    # Init Dataset
    Dataset = {}
    # Generate random dataset
    X, y = make_blobs(n_samples=N, n_features=dim, centers=centers, random_state=42)
    Dataset["points"] = np.array(X)
    Dataset["labels"] = np.array(y)
    Dataset["unique_labels"] = np.unique(Dataset["labels"])
    Dataset["dim"] = dim

    # Plot the dataset
    if plot:
        PlotLabelledData(Dataset, title="Random Blobs", plot=True)

    return Dataset

def GeneratePointsFromImage(I, plot=False):
    '''
    Generates a dataset of points from an image.
    '''
    # Init Dataset
    Dataset = {}
    # Assign binary image
    I_bin = np.array(I)
    # Get points
    points = list(zip(*np.where(I_bin)))
    points = np.array(points)
    Dataset["points"] = points
    Dataset["labels"] = np.zeros(points.shape[0], dtype=int)
    Dataset["unique_labels"] = np.unique(Dataset["labels"])
    Dataset["dim"] = 2

    # Plot the dataset
    if plot:
        PlotLabelledData(Dataset, title="Image Points", plot=True)

    return Dataset

def GeneratePolynomialDistributionData(N, x_dim, y_dim, valRange=[-1.0, 1.0]):
    '''
    Generates a dataset of Xs with Y = poly(X).
    '''
    # Init Dataset
    Dataset = {}
    # Generate random dataset
    X = np.random.uniform(valRange[0], valRange[1], (N, x_dim))

    Ys = []
    for i in range(y_dim):
        randomPolyDegree = np.random.randint(-5, 6)
        randomCoeffs = np.random.uniform(-1.0, 1.0, (x_dim + 1))
        Y = np.sum(randomCoeffs[1:] * (X**randomPolyDegree), axis=-1) + randomCoeffs[0]
        Ys.append(Y)
    Ys = np.dstack(Ys)[0]
    Dataset["X"] = np.array(X)
    Dataset["Y"] = np.array(Ys)
    Dataset["X_dim"] = x_dim
    Dataset["Y_dim"] = y_dim

    return Dataset

def GeneratePolynomialNoisyData_2D(N, degree, noise_factor=0.5, valRange=[-1.0, 1.0], coeffValRange=[-1.0, 1.0]):
    '''
    Generates a dataset of Xs with Y = poly(X) with noise.
    '''
    # Init Dataset
    Dataset = {}
    # Generate random dataset
    X = np.random.uniform(valRange[0], valRange[1], N)

    randomCoeffs = np.random.uniform(coeffValRange[0], coeffValRange[1], (degree + 1))
    Y = np.zeros(N)
    for i in range(degree+1):
        Y += randomCoeffs[i] * (X**i) + np.random.normal(0, noise_factor, N)

    Dataset["X"] = np.array(X)
    Dataset["Y"] = np.array(Y)
    Dataset["degree"] = degree

    return Dataset

# Graph Datasets
def GenerateRandomAdjacencyMatrix(N, prob_edge=0.5, weight_range=[0.1, 1.0], weights_int_only=False, no_self_loops=True, undirected=True):
    '''
    Generates a random adjacency matrix.
    '''
    # Generate random adjacency matrix
    Adj = np.random.uniform(low=weight_range[0], high=weight_range[1], size=(N, N))
    Adj_mask = np.random.uniform(low=0.0, high=1.0, size=(N, N)) > prob_edge
    Adj[Adj_mask] = np.inf
    if weights_int_only:
        Adj = np.round(Adj, decimals=0)
    if no_self_loops:
        Adj[np.diag_indices(N)] = np.inf
    if undirected:
        for i in range(N):
            for j in range(N):
                Adj[i, j] = min(Adj[i, j], Adj[j, i])
    return Adj

def GenerateJSONDataFromAdjacencyMatrix(Adj):
    '''
    Generates jsonData from a adjacency matrix.
    '''
    # Generate jsonData
    AdjData = Adj.tolist()
    for i in range(len(AdjData)):
        for j in range(len(AdjData[i])):
            if AdjData[i][j] == np.inf:
                AdjData[i][j] = "inf"
    jsonData = {"adjacency_matrix": AdjData}
    jsonData = json.dumps(jsonData, indent=4)
    return jsonData

def GenerateAdjacencyMatrixFromJSONData(jsonData):
    '''
    Generates a adjacency matrix from jsonData.
    '''
    # Generate adjacency matrix
    AdjData = jsonData["adjacency_matrix"]
    for i in range(len(AdjData)):
        for j in range(len(AdjData[i])):
            if AdjData[i][j] == "inf":
                AdjData[i][j] = np.inf
    Adj = np.array(AdjData)
    return Adj

def DirectReturn(data):
    '''
    Directly returns the data.
    '''
    return data

# Driver Code
# Params

# Params

# RunCode
# Data = GenerateRandomAdjacencyMatrix(5, prob_edge=0.5, weight_range=[-10, 10], weights_int_only=True)
# jsonData = GenerateJSONDataFromAdjacencyMatrix(Data)
# print(jsonData)