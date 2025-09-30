"""
K Means Clustering Algorithm
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
from stqdm import stqdm

from sklearn.cluster import KMeans

from .._Libraries import DatasetGenerators
from .._Libraries import VideoUtils

# Main Functions
# Evaluation and Visualization
def Animate_KMeansConvergence(Dataset, Results, savePath, duration=2.0, use_stqdm=False):
    '''
    Animate KMeans Convergence and save as Video/GIF
    '''
    TQDM = stqdm if use_stqdm else tqdm
    trace = Results["trace"]

    # Generate Plot Images
    Is = []
    Dataset_iter = deepcopy(Dataset)
    for i in TQDM(range(len(trace))):
        iterData = trace[i]
        Dataset_iter["labels"] = iterData["labels"]
        Dataset_iter["unique_labels"] = np.unique(Dataset_iter["labels"])
        Dataset_iter["centers"] = iterData["centers"]
        I_plot = DatasetGenerators.PlotLabelledData(Dataset_iter, title="KMeans Trace Iteration " + str(iterData["iter"]), plot=False)
        Is.append(I_plot)

    # Save Video/GIF
    fps = len(Is)/duration
    VideoUtils.SaveFrames2Video(Is, savePath, fps=fps)

# KMeans
def KMeansClustering(Dataset, K, max_iters=300, use_stqdm=False):
    '''
    K Means Clustering Algorithm
    '''
    TQDM = stqdm if use_stqdm else tqdm
    # Initialize
    # Init K centers as K random points from the dataset
    centers = np.array(Dataset["points"])
    centers = np.random.permutation(centers)
    centers = centers[:K]
    # centers = np.zeros(centers.shape) # Uncomment if all centers to start from Origin
    # Init Labels as 0
    labels = np.zeros(len(Dataset["labels"]))
    # Init previous labels and centers
    labels_prev = np.zeros(len(Dataset["labels"]))
    centers_prev = np.zeros(centers.shape)
    # Trace
    trace = []

    for i in TQDM(range(max_iters)):
        # Calculate distance of each point from each center and assign the point to the closest center
        for j in range(len(Dataset["points"])):
            distances = np.zeros(K)
            for k in range(K):
                distances[k] = np.linalg.norm(centers[k] - Dataset["points"][j])
            labels[j] = np.argmin(distances)
        
        # Store Trace
        iterData = {"iter": i+1, "centers": deepcopy(centers), "labels": deepcopy(labels)}
        trace.append(iterData)

        # Update centers - average of all points assigned to the center
        for k in range(K):
            centers_prev[k] = deepcopy(centers[k])
            if Dataset["points"][labels == k].shape[0] > 0:
                centers[k] = np.mean(Dataset["points"][labels == k], axis=0)

        # Check convergence
        if (np.array_equal(labels, labels_prev) and np.array_equal(centers, centers_prev)):
            break
        else:
            labels_prev = deepcopy(labels)
            centers_prev = deepcopy(centers)

    # Remap Points to final closest centers
    for j in range(len(Dataset["points"])):
        distances = np.zeros(K)
        for k in range(K):
            distances[k] = np.linalg.norm(centers[k] - Dataset["points"][j])
        labels[j] = np.argmin(distances)
    # Store Final Clusters
    iterData = {"iter": len(trace), "centers": deepcopy(centers), "labels": deepcopy(labels)}
    trace.append(iterData)

    # Return
    Results = {}
    Results["labels_pred"] = labels
    Results["centers_pred"] = centers
    Results["trace"] = trace
    return Results

def KMeansClustering_Library(Dataset, K, max_iters=300):
    '''
    K Means Clustering using sklearn Library
    '''
    kmeans = KMeans(n_clusters=K, max_iter=max_iters, random_state=0)
    labels_pred = kmeans.fit_predict(Dataset["points"])
    centers_pred = kmeans.cluster_centers_

    Results = {}
    Results["labels_pred"] = np.array(labels_pred)
    Results["centers_pred"] = np.array(centers_pred)
    return Results

# Driver Code