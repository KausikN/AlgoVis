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
from Algorithms.SequenceAlgos.DigitSeries import *
from Algorithms.SequenceAlgos.FibonacciSequence import *

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
def ParseListString(data, dtype=int):
    listData = [dtype(x.strip()) for x in data.split(",")]
    return listData

# Main Functions


# UI Functions
def UI_DisplaySingleTrace(trace, title=""):
    fig = plt.figure()
    plt.plot(trace)
    plt.scatter(list(range(len(trace))), trace)
    plt.xlabel("Iteration")
    plt.ylabel("Value")
    plt.title(title)
    st.plotly_chart(fig, use_container_width=True)

def UI_DisplayRangeTraces(traces, title=""):
    startVals = [trace[0] for trace in traces]
    itCounts = [len(trace) for trace in traces]
    fig = plt.figure()
    plt.plot(startVals, itCounts)
    plt.scatter(startVals, itCounts)
    plt.xlabel("Start Value")
    plt.ylabel("Iterations")
    plt.title(title)
    st.plotly_chart(fig, use_container_width=True)

def UI_SingleValueConvergence(ConvergeFunc, title=""):
    USERINPUT_startVal = st.number_input("Enter Starting Value", 1, 99999, 23, 1)
    annotate = False

    if st.button("Visualise"):
        # Process Inputs
        trace, iterCount, I_plot = SVL.Series_ValueConvergeVis(ConvergeFunc, USERINPUT_startVal, titles=["", "", ""], annotate=annotate, plot=False)

        # Display Outputs
        st.markdown("## Single Value Trace")
        colSize = (1, 3)
        col1, col2 = st.columns(colSize)
        col1.markdown("Number of Iterations")
        col2.markdown("``` " + str(iterCount) + " ```")
        UI_DisplaySingleTrace(trace, title + " Convergence for " + str(USERINPUT_startVal))

def UI_RangeConvergence(ConvergeFunc, title=""):
    USERINPUT_startRange = st.number_input("Enter Range Start", 1, 99999, 2, 1)
    USERINPUT_endRange = st.number_input("Enter Range End", USERINPUT_startRange, 99999, 23, 1)
    USERINPUT_rangeSkip = st.number_input("Enter Range Skip", 1, int((USERINPUT_endRange - USERINPUT_startRange)/2), 1, 1)

    if st.button("Visualise"):
        # Process Inputs
        computeRange = (USERINPUT_startRange, USERINPUT_endRange, USERINPUT_rangeSkip)
        traces, iters, I_plot = SVL.Series_RangeConvergeVis(ConvergeFunc, computeRange, plotSkip=1, titles=["", "", ""], plot=False)

        # Display Outputs
        st.markdown("## Range Iterations")
        # st.image(I_plot, "Range Iterations", use_column_width=True)
        UI_DisplayRangeTraces(traces, "Values vs " + title + " Convergence Iterations")

# Repo Based Functions
def collatz_conjecture():
    # Title
    st.header("Collatz Conjecture")

    # Load Inputs
    USERINPUT_Mode = st.selectbox("Select Mode", ["Converge Single Value", "Converge Range of Values"])

    # Process Inputs
    ConvergeFunc = functools.partial(CollatzConjecture_Converge, max_iters=-1)
    if USERINPUT_Mode == "Converge Single Value":
        UI_SingleValueConvergence(ConvergeFunc, "Collatz")
    elif USERINPUT_Mode == "Converge Range of Values":
        UI_RangeConvergence(ConvergeFunc, "Collatz")

def digit_series():
    # Title
    st.header("Digit Series")

    # Load Inputs
    USERINPUT_Series = st.selectbox("Select Series", list(DIGITSERIES_FUNCS.keys()))
    USERINPUT_Mode = st.selectbox("Select Mode", ["Converge Single Value", "Converge Range of Values"])

    # Process Inputs
    USERINPUT_SeriesFunc = DIGITSERIES_FUNCS[USERINPUT_Series]
    if USERINPUT_Mode == "Converge Single Value":
        UI_SingleValueConvergence(USERINPUT_SeriesFunc, USERINPUT_Series)
    elif USERINPUT_Mode == "Converge Range of Values":
        UI_RangeConvergence(USERINPUT_SeriesFunc, USERINPUT_Series)

def fibonacci_series():
    # Title
    st.header("Fibonacci Series")

    # Load Inputs
    USERINPUT_Series = st.selectbox("Select Fibonacci Variant", list(FIBONACCISERIES_FUNCS.keys()))

    # Process Inputs
    USERINPUT_SeriesFunc = FIBONACCISERIES_FUNCS[USERINPUT_Series]
    USERINPUT_iters = st.number_input("Enter Iterations", 1, 250, 5, 1)
    USERINPUT_startVals = st.text_input("Enter Starting Values", "1, 1")
    USERINPUT_startVals = ParseListString(USERINPUT_startVals, int)

    ConvergeFunc = functools.partial(USERINPUT_SeriesFunc, startVals=USERINPUT_startVals)
    annotate = False
    if st.button("Visualise"):
        # Process Inputs
        trace, iterCount, I_plot = SVL.Series_ValueConvergeVis(ConvergeFunc, USERINPUT_iters, titles=["", "", ""], annotate=annotate, plot=False)

        # Display Outputs
        st.markdown("## Single Value Trace")
        colSize = (1, 3)
        col1, col2 = st.columns(colSize)
        col1.markdown("Number of Iterations")
        col2.markdown("``` " + str(iterCount) + " ```")
        UI_DisplaySingleTrace(trace, "Fibonacci Series")
    
#############################################################################################################################
# Driver Code
main_SequenceAlgos()