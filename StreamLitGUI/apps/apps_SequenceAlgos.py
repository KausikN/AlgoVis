"""
Stream lit GUI for Sequence Algorithms
"""

# Imports
# import os
# import cv2
import streamlit as st
# import json
# import subprocess
# import functools

from matplotlib import pyplot as plt
from Algorithms.SequenceAlgos.CollatzConjecture import *

# Main Functions
def main_SequenceAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose Sequence Algorithm',
        tuple(
            SUBAPP_MODES
        )
    )

    # Add Functions
    correspondingFuncName = selected_box.replace(' ', '_').lower()
    if correspondingFuncName in globals().keys():
        globals()[correspondingFuncName]()

#############################################################################################################################
# Repo Based Vars


# Util Vars


# Util Functions


# Main Functions


# UI Functions
def UI_DisplaySingleTrace(trace):
    fig = plt.figure()
    plt.plot(trace)
    plt.scatter(list(range(len(trace))), trace)
    plt.xlabel("Iteration")
    plt.ylabel("Value")
    plt.title("Collatz Convergence for " + str(trace[0]))
    st.plotly_chart(fig, use_container_width=True)

def UI_DisplayRangeTraces(traces):
    startVals = [trace[0] for trace in traces]
    itCounts = [len(trace) for trace in traces]
    fig = plt.figure()
    plt.plot(startVals, itCounts)
    plt.scatter(startVals, itCounts)
    plt.xlabel("Start Value")
    plt.ylabel("Convergence Iterations")
    plt.title("Values vs Collatz Convergence Time")
    st.plotly_chart(fig, use_container_width=True)

# Repo Based Functions
def collatz_conjecture():
    # Title
    st.header("Collatz Conjecture")

    # Load Inputs
    USERINPUT_Mode = st.selectbox("Select Mode", ["Converge Single Value", "Converge Range of Values"])

    if USERINPUT_Mode == "Converge Single Value":
        USERINPUT_startVal = st.number_input("Enter Starting Value", 1, 99999, 23, 1)
        USERINPUT_maxIters = -1
        annotate = False

        if st.button("Visualise"):
            # Process Inputs
            ConvergeFuncSingle = functools.partial(CollatzConjecture_Converge, max_iters=USERINPUT_maxIters)
            trace, iterCount, I_plot = SVL.Series_ValueConvergeVis(ConvergeFuncSingle, USERINPUT_startVal, titles=['Iteration', 'Value', "Collatz Convergence for " + str(USERINPUT_startVal)], annotate=annotate, plot=False)

            # Display Outputs
            st.markdown("## Single Value Trace")
            colSize = (1, 3)
            col1, col2 = st.columns(colSize)
            col1.markdown("Number of Iterations")
            col2.markdown("``` " + str(iterCount) + " ```")
            # st.image(I_plot, "Single Value Trace", use_column_width=True)
            UI_DisplaySingleTrace(trace)

    if USERINPUT_Mode == "Converge Range of Values":
        USERINPUT_startRange = st.number_input("Enter Range Start", 1, 99999, 2, 1)
        USERINPUT_endRange = st.number_input("Enter Range End", USERINPUT_startRange, 99999, 23, 1)
        USERINPUT_rangeSkip = st.number_input("Enter Range Skip", 1, int((USERINPUT_endRange - USERINPUT_startRange)/2), 1, 1)
        USERINPUT_maxIters = -1

        if st.button("Visualise"):
            # Process Inputs
            computeRange = (USERINPUT_startRange, USERINPUT_endRange, USERINPUT_rangeSkip)
            ConvergeFuncManyValues = functools.partial(CollatzConjecture_Converge, max_iters=USERINPUT_maxIters)
            traces, iters, I_plot = SVL.Series_RangeConvergeVis(ConvergeFuncManyValues, computeRange, plotSkip=1, titles=['Start Value', 'Convergence Iterations Count', 'Values vs Collatz Convergence Time'], plot=False)

            # Display Outputs
            st.markdown("## Range Iterations")
            # st.image(I_plot, "Range Iterations", use_column_width=True)
            UI_DisplayRangeTraces(traces)
    
#############################################################################################################################
# Driver Code
main_SequenceAlgos()