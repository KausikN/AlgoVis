"""
Stream lit GUI for Classifier Algorithms
"""

# Imports
# import os
# import cv2
# import numpy as np
import streamlit as st
# import json
# import subprocess
# import functools

from Algorithms.ClassificationAlgos.LinearRegression import *

# Main Functions
def main_ClassificationAlgos():
    SUBAPP_MODES = config_subapp["ALGORITHMS"]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose Classification Algorithm',
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


# Repo Based Functions
def linear_regression():
    global DEFAULT_VIDEO_DURATION

    # Title
    st.header("Linear Regression")

    # Prereq Loaders

    # Load Inputs
    st.markdown("## Data Generation Inputs")
    col1, col2, col3 = st.columns(3)
    USERINPUT_N = col1.number_input("Number of Points", 2, 10000, 3, 1)
    USERINPUT_TrueDegree = col2.number_input("True Degree of Points", 1, 100, 1, 1)
    USERINPUT_NoiseFactor = col3.number_input("Noise Factor", 0.0, 1.0, 0.5, 0.01)

    st.markdown("## Regression Inputs")
    USERINPUT_RegDegrees = st.slider("Choose Regression Degrees Range", 1, 100, (1, 2), 1)

    # Process Inputs
    if st.button("Visualise"):
        # Generate Dataset
        Dataset = DatasetGenerators.GeneratePolynomialNoisyData_2D(
            N=USERINPUT_N, degree=USERINPUT_TrueDegree, noise_factor=USERINPUT_NoiseFactor, valRange=[-1.0, 1.0], coeffValRange=[-1.0, 1.0]
        )

        # Run Polynomial Regressions
        degrees_coeffs = []
        for i in range(USERINPUT_RegDegrees[0], USERINPUT_RegDegrees[1] + 1):
            coeffs = PolynomialRegression(Dataset['X'], Dataset['Y'], i)
            degrees_coeffs.append(coeffs)
        # Find Errors
        errors = GetErrors(Dataset['X'], Dataset['Y'], degrees_coeffs)
        best_coeffs_index = np.argmin(errors)

        # Generate and Display Classification Images
        col1, col2 = st.columns(2)
        col1.markdown("Best Fit Polynomial - Degree " + str(USERINPUT_RegDegrees[0] + best_coeffs_index))
        col2.markdown("```python\n" + DisplayPolynomial(degrees_coeffs[best_coeffs_index]))

        degrees = np.arange(USERINPUT_RegDegrees[0], USERINPUT_RegDegrees[1] + 1)
        I_regCurves, fig_regCurves = PlotRegressionCurves(
            Dataset['X'], Dataset['Y'], degrees_coeffs, 
            degrees=degrees, title='Regression Curves'
        )
        # st.image(I_regCurves, caption="Regression Curves", use_column_width=True)
        st.plotly_chart(fig_regCurves, use_container_width=True)

        I_errors, fig_errors = PlotErrors(errors, degrees, title='Degrees vs Errors')
        # st.image(I_errors, caption="Degrees vs Errors", use_column_width=True)
        st.plotly_chart(fig_errors, use_container_width=True)
    
#############################################################################################################################
# Driver Code
main_ClassificationAlgos()