"""
Neural Network Visualiser
"""

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Main Functions
# Utils Functions
def DisplayImage(I, title=""):
    plt.imshow(I)
    plt.title(title)
    plt.show()

def GetRatio(val, valRange):
    '''
    Gets the ratio of a value to a range
    '''
    if valRange[0] == valRange[1]:
        return 1.0
    return abs((val - valRange[0]) / (valRange[1] - valRange[0]))

def CombineColors(col1, col2):
    '''
    Combines col1 with col2 based on alpha of col1
    '''
    a1 = col1[3]
    # a2 = col2[3]
    a2 = 255 - a1
    amuls = [a1 / (a1 + a2), a2 / (a1 + a2)]
    combCol = [(col1[i]*amuls[0] + col2[i]*amuls[1]) for i in range(len(col1)-1)]
    combCol.append(max(a1, a2))
    # combCol = np.array(combCol, dtype=int)

    return combCol

# Generate Network Functions
def GenerateRandomNetwork(layer_sizes):
    '''
    Generates a network from a list of layer sizes
    '''

    # Random Params
    RANDOM_NODES_RANGE= (-1.0, 1.0)
    RANDOM_WEIGHTS_RANGE= (-1.0, 1.0)

    # Network Params
    n_layers = len(layer_sizes)
    nodes = []
    weights = []
    biases = []

    # Generate Nodes
    for layer in range(n_layers):
        nodeVals = np.random.uniform(RANDOM_NODES_RANGE[0], RANDOM_NODES_RANGE[1], layer_sizes[layer])
        nodes.append(list(nodeVals))

    # Generate Weights
    for layer in range(n_layers - 1):
        weights_layer = np.random.uniform(RANDOM_WEIGHTS_RANGE[0], RANDOM_WEIGHTS_RANGE[1], (layer_sizes[layer], layer_sizes[layer+1]))
        weights.append(list(weights_layer))

    # Generate Biases
    for layer in range(n_layers - 1):
        biases_layer = np.random.uniform(RANDOM_WEIGHTS_RANGE[0], RANDOM_WEIGHTS_RANGE[1], (1, layer_sizes[layer+1]))
        biases.append(list(biases_layer))

    network = {
        "nodes": nodes,
        "weights": weights,
        "biases": biases,
        "node_range": RANDOM_NODES_RANGE,
        "weight_range": RANDOM_WEIGHTS_RANGE
    }
    return network

def GenerateFullNetwork(layer_sizes):
    '''
    Generates a network from a list of layer sizes with all weights and nodes set to 1 (For visualising the network)
    '''
    # Network Params
    n_layers = len(layer_sizes)
    nodes = []
    weights = []
    biases = []

    # Generate Nodes
    for layer in range(n_layers):
        nodeVals = np.ones(layer_sizes[layer])
        nodes.append(list(nodeVals))

    # Generate Weights
    for layer in range(n_layers - 1):
        weights_layer = np.ones((layer_sizes[layer], layer_sizes[layer+1]))
        weights.append(list(weights_layer))

    # Generate Biases
    for layer in range(n_layers - 1):
        biases_layer = np.ones((1, layer_sizes[layer+1]))
        biases.append(list(biases_layer))

    network = {
        "nodes": nodes,
        "weights": weights,
        "biases": biases,
        "node_range": [0.0, 1.0],
        "weight_range": [0.0, 1.0]
    }
    return network

# Generate Functions
def GenerateNetworkImage(network):
    '''
    Generates an image of the network
    '''
    # print()
    # print("GEN IMAGE")
    # print("NODES:", network["nodes"])
    # print("WEIGHTS", network["weights"])

    # Image Params
    IMAGE_SIZE = (1024, 1024)
    IMAGE_PADDING = (0.1, 0.1)
    NODE_PADDING_RATIO = (0.5, 0.25)

    IMAGE_COLOR_BG = (0, 0, 0, 255)
    IMAGE_COLOR_FG = (255, 255, 255, 255)
    NODE_COLOR_BIAS = (0, 0, 255, 255)
    NODE_COLOR_POSITIVE = (0, 255, 0, 255)
    NODE_COLOR_NEGATIVE = (255, 0, 0, 255)
    CONNECTION_COLOR_POSITIVE = (0, 255, 0, 255)
    CONNECTION_COLOR_NEGATIVE = (255, 0, 0, 255)

    NODE_OUTLINE_THICKNESS = 0.005
    CONNECTION_MAX_THICKNESS = 0.025

    # Network Params
    # Get the number of nodes in each layer and number of layers
    network_layer_sizes = np.array([len(network["nodes"][i]) for i in range(len(network["nodes"]))])
    n_layers = network_layer_sizes.shape[0]
    nodes_values = network["nodes"]
    weights = network["weights"]
    biases = network["biases"]

    # Find Node Maximum Allowed Radius
    x_inc = (1 / (n_layers + 1))
    y_inc = (1 / (np.max(network_layer_sizes) + 1 + 1))
    node_r_x = x_inc * NODE_PADDING_RATIO[0]
    node_r_y = y_inc * NODE_PADDING_RATIO[1]
    NODE_RADIUS = int(min(node_r_x * IMAGE_SIZE[0], node_r_y * IMAGE_SIZE[1]) / 2)

    NODES_POSITIONS = []
    for layer in range(n_layers):
        row = []
        pos_x = (layer + 1) * x_inc
        biasAdd = 1 if (layer < (n_layers-1)) else 0
        for node in range(network_layer_sizes[layer] + biasAdd):
            pos_y = (node + 1) * y_inc
            row.append((pos_x, pos_y))
        NODES_POSITIONS.append(row)
    
    I = (np.ones((IMAGE_SIZE[0], IMAGE_SIZE[1], 4), dtype=np.uint8) * IMAGE_COLOR_BG).astype(np.uint8)
    
    # Generate Connections
    weight_range = [0, np.max(np.abs(network["weight_range"]))]
    # Weights
    for layer in range(n_layers - 1):
        for node in range(network_layer_sizes[layer]):
            for next_node in range(network_layer_sizes[layer + 1]):
                pos_1 = tuple([int(NODES_POSITIONS[layer][node][i] * IMAGE_SIZE[i]) for i in range(len(IMAGE_SIZE))])
                pos_2 = tuple([int(NODES_POSITIONS[layer+1][next_node][i] * IMAGE_SIZE[i]) for i in range(len(IMAGE_SIZE))])
                
                LINE_COLOR = CONNECTION_COLOR_POSITIVE if weights[layer][node][next_node] > 0 else CONNECTION_COLOR_NEGATIVE
                
                wRatio = GetRatio(abs(weights[layer][node][next_node]), weight_range)
                if wRatio > 1.0:
                    print(layer, node, next_node, wRatio, weights[layer][node][next_node], weight_range)
                LINE_THICKNESS = wRatio * CONNECTION_MAX_THICKNESS * min(IMAGE_SIZE)
                LINE_THICKNESS = max(1, int(round(LINE_THICKNESS, 0)))
                # print("W:", layer, node, next_node, weights[layer][node][next_node], LINE_COLOR, LINE_THICKNESS)

                if LINE_THICKNESS > 0:
                    I = np.array(cv2.line(I, pos_1, pos_2, LINE_COLOR, LINE_THICKNESS), dtype=np.uint8)

    # Biases
    for layer in range(n_layers - 1):
        for next_node in range(network_layer_sizes[layer+1]):
            pos_1 = tuple([int(NODES_POSITIONS[layer][network_layer_sizes[layer]][i] * IMAGE_SIZE[i]) for i in range(len(IMAGE_SIZE))])
            pos_2 = tuple([int(NODES_POSITIONS[layer+1][next_node][i] * IMAGE_SIZE[i]) for i in range(len(IMAGE_SIZE))])
            
            LINE_COLOR = CONNECTION_COLOR_POSITIVE if biases[layer][0][next_node] > 0 else CONNECTION_COLOR_NEGATIVE

            bRatio = GetRatio(abs(biases[layer][0][next_node]), weight_range)
            if bRatio > 1.0:
                print(layer, next_node, bRatio, biases[layer][0][next_node], weight_range)
            LINE_THICKNESS = bRatio * CONNECTION_MAX_THICKNESS * min(IMAGE_SIZE)
            LINE_THICKNESS = max(1, int(round(LINE_THICKNESS, 0)))
            # print("B:", layer, next_node, biases[layer][0][next_node], LINE_COLOR, LINE_THICKNESS)

            if LINE_THICKNESS > 0:
                I = np.array(cv2.line(I, pos_1, pos_2, LINE_COLOR, LINE_THICKNESS), dtype=np.uint8)

    # Generate Node Circles
    for layer in range(n_layers):
        for node in range(network_layer_sizes[layer]):
            pos = tuple([int(NODES_POSITIONS[layer][node][i] * IMAGE_SIZE[i]) for i in range(len(IMAGE_SIZE))])

            NODE_COLOR = list(NODE_COLOR_POSITIVE) if nodes_values[layer][node] > 0 else list(NODE_COLOR_NEGATIVE)
            node_val_range = [0, np.max(np.abs(network["node_range"]))]
            NODE_ALPHA = GetRatio(nodes_values[layer][node], node_val_range)
            NODE_COLOR[3] = int(NODE_ALPHA * NODE_COLOR[3])
            NODE_COLOR = tuple(CombineColors(NODE_COLOR, IMAGE_COLOR_BG))
            # NODE_COLOR = tuple(NODE_COLOR)
            # print("NODE:", layer, node, nodes_values[layer][node], NODE_COLOR)

            # Filled Circle
            I = np.array(cv2.circle(I, pos, NODE_RADIUS, NODE_COLOR, -1), dtype=np.uint8)
            # Outline Circle
            NODE_OUTLINE = max(1, int(NODE_OUTLINE_THICKNESS * min(IMAGE_SIZE)))
            I = np.array(cv2.circle(I, pos, NODE_RADIUS, IMAGE_COLOR_FG, NODE_OUTLINE), dtype=np.uint8)

    # Generate Node Circles for Bias Nodes
    for layer in range(n_layers - 1):
        pos = tuple([int(NODES_POSITIONS[layer][network_layer_sizes[layer]][i] * IMAGE_SIZE[i]) for i in range(len(IMAGE_SIZE))])
        NODE_COLOR = tuple(NODE_COLOR_BIAS)
        # Filled Circle
        I = np.array(cv2.circle(I, pos, NODE_RADIUS, NODE_COLOR, -1), dtype=np.uint8)
        # Outline Circle
        NODE_OUTLINE = max(1, int(NODE_OUTLINE_THICKNESS * min(IMAGE_SIZE)))
        I = np.array(cv2.circle(I, pos, NODE_RADIUS, IMAGE_COLOR_FG, NODE_OUTLINE), dtype=np.uint8)

    return I

# Driver Code
# # Params
# NetworkSizes = [2, 4, 2]
# # Params

# # RunCode
# Network = GenerateRandomNetwork(NetworkSizes)
# I = GenerateNetworkImage(Network)
# DisplayImage(I, "Network " + str(NetworkSizes))