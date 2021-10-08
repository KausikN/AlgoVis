'''
Simple Fully Connected Neural Network
'''

# Imports
import cv2
import json
import functools
import numpy as np
from tqdm import tqdm

from .Libraries import VideoUtils
from .Libraries import NetworkVis
from .Libraries import DatasetGenerators
from .FunctionsLibrary import LossFunctions
from .FunctionsLibrary import ActivationFunctions

# Utils Functions
def GenerateHistoryVideo(history, savePath, duration=2.0):
    Is = []

    print("Nodes Diff:")
    NodesSame = []
    for i in range(len(history["nodes"])-1):
        diffs = []
        for layer in range(len(history["nodes"][i])):
            diffs.append(np.sum(np.abs(np.array(history["nodes"][i][layer]) - np.array(history["nodes"][i+1][layer]))))
        NodesSame.append(np.round(np.max(diffs), 2))
    print(NodesSame)
    print("\n\n")

    print("Ws Diff:")
    WsSame = []
    for i in range(len(history["Ws"])-1):
        diffs = []
        for layer in range(len(history["Ws"][i])):
            diffs.append(np.sum(np.abs(np.array(history["Ws"][i][layer]) - np.array(history["Ws"][i+1][layer]))))
        WsSame.append(np.round(np.max(diffs), 2))
    print(WsSame)
    print("\n\n")

    print("Generating", history["n_iters"], "frames...")
    for i in tqdm(range(history["n_iters"])):
        nodes_vals = []
        for j in range(len(history["nodes"][i])):
            nodes_vals.extend(history["nodes"][i][j])
        nodes_range = [min(nodes_vals), max(nodes_vals)]

        weights_vals = []
        for j in range(len(history["Ws"][i])):
            flat_ws = np.array(history["Ws"][i][j]).flatten()
            weights_vals.extend(flat_ws)
        weights_range = [min(weights_vals), max(weights_vals)]

        network = {
            'nodes': history["nodes"][i],
            'weights': history["Ws"][i],
            'node_range': nodes_range,
            'weight_range': weights_range
        }
        I = NetworkVis.GenerateNetworkImage(network)
        I_rgb = np.array(I[:, :, :3], dtype=np.uint8)
        # Add iteration text
        itText = str(i) + "/" + str(history["n_iters"]) + ": " + str(round(history["loss"][i], 2))
        I_rgb = VideoUtils.ImageAddText(I_rgb, itText)
        I_rgb = cv2.cvtColor(I_rgb, cv2.COLOR_BGR2RGB)
        Is.append(I_rgb)

    fps = len(Is) / duration
    VideoUtils.SaveFrames2Video(Is, savePath, fps)

def PlotFunctionAndDerivative(fn_name, fn, fn_deriv, valRange=[0.0, 1.0], N=100):
    Xs = np.linspace(valRange[0], valRange[1], N)

    # Function Plot
    Ys = np.array([fn(X) for X in Xs])
    Points = np.dstack((Xs, Ys))[0]
    Dataset = {
        "points": Points,
        "dim": 2
    }
    fn_title = fn_name + " Function Plot"
    I_fn = DatasetGenerators.PlotUnlabelledData(Dataset, fn_title, lines=True, plot=False)

    # Function Derivative Plot
    Ys_deriv = np.array([fn_deriv(X) for X in Xs])
    Points_deriv = np.dstack((Xs, Ys_deriv))[0]
    Dataset_deriv = {
        "points": Points_deriv,
        "dim": 2
    }
    fn_deriv_title = fn_name + " Deriv" + " Function Plot"
    I_fn_deriv = DatasetGenerators.PlotUnlabelledData(Dataset_deriv, fn_deriv_title, lines=True, plot=False)

    return I_fn, I_fn_deriv

# Main Functions
# Init Functions
def initialize_parameters(layer_sizes, funcs):
    Ws = []
    bs = []
    for i in range(len(layer_sizes)-1):
        W = np.random.randn(layer_sizes[i+1], layer_sizes[i])
        b = 0
        Ws.append(W)
        bs.append(b)

    parameters = {
        "n_layers": len(layer_sizes),
        "layer_sizes": layer_sizes,
        "Ws": Ws,
        "bs" : bs,
        "act_fn": {
            "func": funcs["act_fn"],
            "deriv": funcs["act_fn_deriv"]
        },
        "loss_fn": {
            "func": funcs["loss_fn"],
            "deriv": funcs["loss_fn_deriv"]
        }
    }
    return parameters

# Forward Propagation Functions
def forward_prop(X, parameters):
    As = [list(X.flatten())]

    Ws = parameters["Ws"]
    bs = parameters["bs"]
    act_fn = parameters["act_fn"]["func"]
    # Initial a = x
    a = X
    for i in range(len(Ws)):
        # o = W a(previous layer) + b
        Wa = np.dot(a, Ws[i].T)
        o = Wa + bs[i]
        # a = activation(o)
        a = act_fn(o)
        # Save all activations
        As.append(list(o.flatten()))

    return a, As

# Backward Propogation Functions
def backward_prop(X, y, parameters):
    n_layers = parameters["n_layers"]
    Ws = parameters["Ws"]
    bs = parameters["bs"]
    act_fn = parameters["act_fn"]["func"]
    act_fn_deriv = parameters["act_fn"]["deriv"]
    loss_fn_deriv = parameters["loss_fn"]["deriv"]

    grads = {}
    
    a = X
    node_values = [np.copy(a)]
    # Find final activations
    for i in range(len(Ws)):
        o = np.dot(a, Ws[i].T) + bs[i]
        a = act_fn(o)
        node_values.append(np.copy(a))

    # Find loss Derivative at output layer
    grads["dE"] = loss_fn_deriv(a, y)
    grads["dA"] = act_fn_deriv(a)
    grads["dO"] = []
    for i in range(n_layers):
        grads["dO"].append([])
    grads["dO"][-1] = grads["dE"] * grads["dA"]
    grads["dW"] = []
    grads["db"] = []
    # Find grads of nodes by going from last layer to first layer
    layer_indices = list(reversed(range(n_layers-1)))
    for i in layer_indices:
        dO = grads["dO"][i+1]
        # Find dW
        dW = np.dot(dO.T, node_values[i])
        grads["dW"].insert(0, dW)
        # Find db
        db = np.sum(bs[i] * dO)
        grads["db"].insert(0, db)
        # Find dO for ith layer
        dO_i = np.dot(dO, Ws[i])
        grads["dO"][i] = act_fn_deriv(node_values[i]) * dO_i

    return grads

def update_parameters(parameters, grads, lr):
    Ws = parameters["Ws"]
    bs = parameters["bs"]
    for i in range(len(Ws)):
        Ws[i] -= lr * grads["dW"][i]
        bs[i] -= lr * grads["db"][i]
    parameters["Ws"] = Ws
    parameters["bs"] = bs

    return parameters

# Model Functions
def model(X, Y, layer_sizes, n_epochs, lr, funcs):
    history = {
        "n_iters": n_epochs * X.shape[0],
        "layer_sizes": layer_sizes,
        "nodes": [],
        "Ws": [],
        "bs": [],
        "loss": []
    }

    parameters = initialize_parameters(layer_sizes, funcs)
    for i in tqdm(range(0, n_epochs)):
        for x, y in zip(X, Y):
            x = x.reshape(1, x.shape[0])
            y = y.reshape(1, y.shape[0])

            y_out, As = forward_prop(x, parameters)
            loss = funcs["loss_fn"](y_out, y)[0]
            grads = backward_prop(x, y, parameters)
            parameters = update_parameters(parameters, grads, lr)
            
            # Record History
            # Convert Ws and bs to lists
            bs = parameters["bs"]
            Ws = []
            for W in parameters["Ws"]:
                W = (W.T).tolist()
                Ws.append(W)

            bs = list(bs)
            history["nodes"].append(As)
            history["Ws"].append(Ws)
            history["bs"].append(bs)
            history["loss"].append(loss)

        if(i%1 == 0):
            print(f'EPOCH {i}: {loss}')

    return parameters, history

# Predict Functions
def predict(X, parameters):
    y_pred, _ = forward_prop(X, parameters)
    y_pred = np.squeeze(y_pred)
    return y_pred >= 0.5

# Driver Code
# # Params
# network_layers = [4]

# X = [
#     [0, 0],
#     [0, 1],
#     [1, 0],
#     [1, 1]
# ]
# Y = [[0, 0], [1, 1], [1, 1], [0, 0]]

# learning_rate = 0.3
# n_epochs = 5
# funcs = {
#     "act_fn": ActivationFunctions.sigmoid,
#     "act_fn_deriv": ActivationFunctions.sigmoid_deriv,
#     "loss_fn": LossFunctions.categorical_cross_entropy_error,
#     "loss_fn_deriv": LossFunctions.categorical_cross_entropy_error_deriv
# }

# savePath = "GeneratedVisualisations/Haha.avi"
# duration = 1.0
# # Params

# # RunCode
# X = np.array(X)
# Y = np.array(Y)
# network_layers = [X.shape[1]] + network_layers + [Y.shape[1]]

# # Train Model
# trained_parameters, history = model(X, Y, network_layers, n_epochs, learning_rate, funcs=funcs)

# # Generate Video
# tempSavePath = "GeneratedVisualisations/temp.avi"
# GenerateHistoryVideo(history, tempSavePath, duration)

# # Fix Video
# VideoUtils.FixVideoFile(tempSavePath, savePath)