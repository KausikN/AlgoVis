"""
Stream lit GUI for AI Algorithms
"""

# Imports
import streamlit as st

from Algorithms.AIAlgos.FNN import *

# Main Functions
def main_AIAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose AI Algorithm",
        tuple(
            SUBAPP_MODES
        )
    )

    # Add Functions
    correspondingFuncName = selected_box.replace(" ", "_").lower()
    if correspondingFuncName in globals().keys():
        globals()[correspondingFuncName]()

#############################################################################################################################
# Repo Based Vars

# Util Vars

# Util Functions

# Main Functions
def GetNetworkSize(network_size_str):
    '''
    Get Network Size from string
    '''
    network_size_str = network_size_str.split(",")
    network_size = []
    for size in network_size_str:
        network_size.append(int(size.strip()))
    return network_size

def GenerateDataset(N, x_dim, y_dim, valRange):
    '''
    Generate dataset
    '''
    Dataset = generate_polynomial_dist_data(N, x_dim, y_dim, valRange)
    return Dataset

# UI Functions
def UI_GetNetworkInputs(USERINPUT_DIM_X, USERINPUT_DIM_Y):
    '''
    UI - Get Network Inputs
    '''
    # Network Size
    col1, col2 = st.columns(2)
    USERINPUT_network_size = col1.text_input("Network Size (',' separated sizes of each hidden layer)", "2, 4, 2")
    USERINPUT_NETWORK_SIZES = [USERINPUT_DIM_X] + GetNetworkSize(USERINPUT_network_size) + [USERINPUT_DIM_Y]
    
    NetworkFull = GenerateNeuralNetwork_Full(USERINPUT_NETWORK_SIZES)
    I_NetworkFull = GenerateNeuralNetworkImage(NetworkFull)
    col2.image(I_NetworkFull, use_container_width=True)

    # Functions
    # Activation Function
    col1, col2, col3 = st.columns((1, 1.5, 1.5))
    USERINPUT_ActivationFunc = col1.selectbox("Activation Function", list(ACTIVATION_FUNCS.keys()))
    maxLimit = col1.number_input("Act Func Plot Limit", 0.1, 100.0, 1.0, 0.1)
    I_act_fn, I_act_fn_deriv = PlotFunctionAndDerivative(USERINPUT_ActivationFunc, 
        ACTIVATION_FUNCS[USERINPUT_ActivationFunc]["func"], ACTIVATION_FUNCS[USERINPUT_ActivationFunc]["deriv"], 
        [-maxLimit, maxLimit], 100
    )
    col2.image(I_act_fn, use_container_width=True)
    col3.image(I_act_fn_deriv, use_container_width=True)

    # Output Activation Function
    col1, col2, col3 = st.columns((1, 1.5, 1.5))
    USERINPUT_OutputActivationFunc = col1.selectbox("Output Activation Function", list(ACTIVATION_FUNCS.keys()))
    maxLimit = col1.number_input("Out Act Func Plot Limit", 0.1, 100.0, 1.0, 0.1)
    I_out_act_fn, I_out_act_fn_deriv = PlotFunctionAndDerivative(USERINPUT_OutputActivationFunc, 
        ACTIVATION_FUNCS[USERINPUT_OutputActivationFunc]["func"], ACTIVATION_FUNCS[USERINPUT_OutputActivationFunc]["deriv"], 
        [-maxLimit, maxLimit], 100
    )
    col2.image(I_out_act_fn, use_container_width=True)
    col3.image(I_out_act_fn_deriv, use_container_width=True)

    # Loss Function
    col1, col2, col3 = st.columns((1, 1.5, 1.5))
    USERINPUT_LossFunc = col1.selectbox("Loss Function", list(LOSS_FUNCTIONS.keys()))
    # maxLimit = col1.number_input("Loss Func Plot Limit", 0.1, 100.0, 1.0, 0.1)
    # LossFunc = functools.partial(LOSS_FUNCTIONS[USERINPUT_LossFunc]["func"], t=0.0)
    # LossFuncDeriv = functools.partial(LOSS_FUNCTIONS[USERINPUT_LossFunc]["deriv"], t=0.0)
    # I_loss_fn, I_loss_fn_deriv = PlotFunctionAndDerivative(USERINPUT_LossFunc, LossFunc, LossFuncDeriv, [-maxLimit, maxLimit], 100)
    # col2.image(I_loss_fn, use_container_width=True)
    # col3.image(I_loss_fn_deriv, use_container_width=True)

    return USERINPUT_NETWORK_SIZES, USERINPUT_ActivationFunc, USERINPUT_OutputActivationFunc, USERINPUT_LossFunc

# Repo Based Functions
def feed_forward_neural_network():
    global DEFAULT_VIDEO_DURATION

    # Title
    st.header("Feed Forward Neural Network")

    # Prereq Loaders

    # Load Inputs
    st.markdown("## Data Generation Inputs")
    col1, col2, col3 = st.columns(3)
    USERINPUT_N = col1.number_input("Number of Datapoints", 2, 100, 3, 1)
    USERINPUT_DIM_X = col2.number_input("Number of Input Data Dimensions", 1, 10, 2, 1)
    USERINPUT_DIM_Y = col3.number_input("Number of Output Data Dimensions", 1, 10, 2, 1)

    st.markdown("## Network Inputs")
    USERINPUT_NETWORK_SIZES, USERINPUT_ActivationFunc, USERINPUT_OutputActivationFunc, USERINPUT_LossFunc = UI_GetNetworkInputs(USERINPUT_DIM_X, USERINPUT_DIM_Y)

    st.markdown("## Train Inputs")
    USERINPUT_learning_rate = st.number_input("Learning Rate", 0.01, 100.0, 0.3, 0.01)
    USERINPUT_epochs = st.number_input("Number of Epochs", 1, 100, 1, 1)

    # Process Inputs
    if st.button("Visualise"):
        # Generate Dataset
        Dataset = GenerateDataset(USERINPUT_N, USERINPUT_DIM_X, USERINPUT_DIM_Y, [-1, 1])
        # print(Dataset)
        funcs = {
            "act_fns": 
                [ACTIVATION_FUNCS[USERINPUT_ActivationFunc]] * (len(USERINPUT_NETWORK_SIZES) - 2)
                + [ACTIVATION_FUNCS[USERINPUT_OutputActivationFunc]],
            "loss_fn": LOSS_FUNCTIONS[USERINPUT_LossFunc]["func"],
            "loss_fn_deriv": LOSS_FUNCTIONS[USERINPUT_LossFunc]["deriv"]
        }
        # Train FNN
        trained_parameters, history = model(Dataset["X"], Dataset["Y"], USERINPUT_NETWORK_SIZES, 
            USERINPUT_epochs, USERINPUT_learning_rate, funcs=funcs, 
            use_stqdm=True
        )

        # Generate Video
        GenerateHistoryVideo(history, PATHS["default"]["save"]["video_converted"], DEFAULT_VIDEO_DURATION, use_stqdm=True)
        # GenerateHistoryVideo(history, PATHS["default"]["save"]["video"], DEFAULT_VIDEO_DURATION, use_stqdm=True)
        # Fix Video
        # VideoUtils.FixVideoFile(PATHS["default"]["save"]["video"], PATHS["default"]["save"]["video_converted"])
        # Display Animation Video
        st.video(PATHS["default"]["save"]["video_converted"])
    
#############################################################################################################################
# Run Code
main_AIAlgos()