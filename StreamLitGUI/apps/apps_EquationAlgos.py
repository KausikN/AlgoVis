"""
Stream lit GUI for Equation Algorithms
"""

# Imports
# import os
# import cv2
import streamlit as st
import json
import matplotlib.pyplot as plt
# import subprocess
# import functools

from Algorithms.EquationAlgos.EquationVis import *

# Main Functions
def main_EquationAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose Sort Algorithm",
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


# UI Functions
def UI_TransformFunc(groupNum, st=st):
    '''
    UI - Get Transform Function
    '''
    st.markdown("Transform Function " + str(groupNum))
    # Get Func and Params
    USERINPUT_FuncName = st.selectbox("Function", tuple(TRANSFORM_FUNCS.keys()), key="Func_" + str(groupNum))
    USERINPUT_FuncParamsStr = st.text_input("Parameters", "", key="Param_" + str(groupNum))
    USERINPUT_FuncParams = json.loads("{" + USERINPUT_FuncParamsStr + "}")
    # Construct
    USERINPUT_Func = functools.partial(TRANSFORM_FUNCS[USERINPUT_FuncName], **USERINPUT_FuncParams)
    # Display
    Xs = np.linspace(0.0, 10.0, 100)
    Ys = EquationVis_2D_Generic(Xs, USERINPUT_Func, startPos=0.0, scale=1.0)
    fig = plt.figure()
    plt.plot(Xs, Ys)
    plt.title("Transform Function " + str(groupNum))
    st.plotly_chart(fig, key="Plot_" + str(groupNum))

    return USERINPUT_Func

def UI_ConstructTransformFuncs():
    '''
    UI - Construct Transform Functions
    '''
    st.markdown("### Transform Functions")
    # Get Funcs
    USERINPUT_NGroups = st.number_input("Number of Transform Functions", 1, 3, 1, 1)
    Funcs = []
    cols = st.columns(USERINPUT_NGroups)
    for i in range(USERINPUT_NGroups):
        USERINPUT_Func = UI_TransformFunc(i+1, st=cols[i])
        Funcs.append(USERINPUT_Func)
    # Get Combination
    USERINPUT_CombinationStr = st.text_input("Combination (Use {F1}, {F2}, etc to refer to funcs)", "{F1}")

    return Funcs, USERINPUT_CombinationStr

# Repo Based Functions
def equation_vis():
    # Title
    st.header("Equation Vis")

    # Prereq Loaders

    # Load Inputs
    col1, col2 = st.columns(2)
    USERINPUT_x_start = col1.number_input("X start", value=0.0)
    USERINPUT_x_end = col2.number_input("X end", value=10.0)
    USERINPUT_TransformFunc, USERINPUT_Combination = UI_ConstructTransformFuncs()

    # Process Inputs
    if st.button("Visualise"):
        # Get Ys for Funcs
        Xs = np.linspace(USERINPUT_x_start, USERINPUT_x_end, 100)
        Ys = []
        for USERINPUT_Func in USERINPUT_TransformFunc:
            Ys.append(EquationVis_2D_Generic(Xs, USERINPUT_Func, startPos=0.0, scale=1.0))
        Ys = np.array(Ys)
        Ys_Combined = EquationVis_2D_Combined(Ys, USERINPUT_Combination)
        # Display
        fig = plt.figure()
        plt.plot(Xs, Ys_Combined)
        plt.title("Equation")
        st.plotly_chart(fig)
    
#############################################################################################################################
# Driver Code
main_EquationAlgos()