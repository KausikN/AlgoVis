'''
Simple Fully Connected Neural Network
'''

# Imports
import cv2
import numpy as np
from tqdm import tqdm

from .._Libraries import VideoUtils
from .._Libraries import NetworkVis
from .._Libraries import DatasetGenerators
from .FunctionsLibrary.LossFunctions import *
from .FunctionsLibrary.ActivationFunctions import *

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

    print("Bs Diff:")
    bsSame = []
    for i in range(len(history["bs"])-1):
        diffs = []
        for layer in range(len(history["bs"][i])):
            diffs.append(np.sum(np.abs(np.array(history["bs"][i][layer]) - np.array(history["bs"][i+1][layer]))))
        bsSame.append(np.round(np.max(diffs), 2))
    print(bsSame)
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
        biases_vals = []
        for j in range(len(history["bs"][i])):
            flat_bs = np.array(history["bs"][i][j]).flatten()
            biases_vals.extend(flat_bs)
        biases_range = [min(biases_vals), max(biases_vals)]
        # print() # TODO HERE #######################################################
        weights_range = [min(weights_range[0], biases_range[0]), max(weights_vals[1], biases_vals[1])]

        network = {
            'nodes': history["nodes"][i],
            'weights': history["Ws"][i],
            'biases': history["bs"][i],
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
    # Ys = np.array([fn(X) for X in Xs])
    Ys = np.array(fn(Xs))
    Points = np.dstack((Xs, Ys))[0]
    Dataset = {
        "points": Points,
        "dim": 2
    }
    fn_title = fn_name + " Function Plot"
    I_fn = DatasetGenerators.PlotUnlabelledData(Dataset, fn_title, lines=True, plot=False)

    # Function Derivative Plot
    # Ys_deriv = np.array([fn_deriv(X) for X in Xs])
    Ys_deriv = np.array(fn_deriv(Xs))
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
        # W = np.random.randn(layer_sizes[i+1], layer_sizes[i])
        # b = 0
        # W = np.random.randn(layer_sizes[i], layer_sizes[i+1])
        W = np.zeros((layer_sizes[i], layer_sizes[i+1]))
        b = np.zeros((1, layer_sizes[i+1]))
        Ws.append(W)
        bs.append(b)

    parameters = {
        "n_layers": len(layer_sizes),
        "layer_sizes": layer_sizes,
        "Ws": Ws,
        "bs" : bs,
        "act_fns": funcs["act_fns"],
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
    act_fns = parameters["act_fns"]

    # Initial a = x
    a = X
    for i in range(len(Ws)):
        # o = W a(previous layer) + b
        o = np.dot(a, Ws[i]) + bs[i]
        # a = activation(o)
        a = act_fns[i]["func"](o)
        # Save all activations
        As.append(list(o.flatten()))

    return a, As

# Backward Propogation Functions
def backward_prop(X, y, parameters):
    n_layers = parameters["n_layers"]
    Ws = parameters["Ws"]
    bs = parameters["bs"]
    act_fns = parameters["act_fns"]
    loss_fn_deriv = parameters["loss_fn"]["deriv"]

    grads = {}
    
    # Find final activations
    a = X
    node_values = [np.copy(a)]
    for i in range(len(Ws)):
        o = np.dot(a, Ws[i]) + bs[i]
        a = act_fns[i]["func"](o)
        node_values.append(np.copy(a))

    # Find loss Derivative at output layer
    grads["dW"] = []
    grads["db"] = []
    grads["dE"] = loss_fn_deriv(a, y)
    
    # Find grads of nodes by going from last layer to first layer
    dO = grads["dE"]
    layer_indices = list(reversed(range(n_layers-1)))
    for i in layer_indices:
        # Find dA
        grads["dA"] = act_fns[i]["deriv"](node_values[i+1])
        # Find dO
        dO = dO * grads["dA"]
        # Find dW
        # dW = np.dot(dO.T, node_values[i])
        dW = np.dot(node_values[i].T, dO)
        grads["dW"].insert(0, dW)
        # Find db
        # db = np.sum(bs[i] * dO)
        db = dO
        grads["db"].insert(0, db)
        # Update dO
        dO = np.dot(dO, Ws[i].T)

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
            loss = parameters["loss_fn"]["func"](y_out, y)[0]
            grads = backward_prop(x, y, parameters)
            parameters = update_parameters(parameters, grads, lr)
            
            # Record History
            # Convert Ws and bs to lists
            bs = []
            Ws = []
            for W in parameters["Ws"]:
                W = (W).tolist()
                Ws.append(W)
            for b in parameters["bs"]:
                b = (b).tolist()
                bs.append(b)

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