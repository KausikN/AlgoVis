"""
Stream lit GUI for Classifier Algorithms
"""

# Imports
from streamlit_common_utils._common import DictData
from streamlit_common_utils.streamlit_common_ui_setup import *

from .LinearRegression import *

# Main Functions
def main(selected="Classification Algorithms", MODES=[], global_override_vars=None, **kwargs):
    # Update global variables
    if global_override_vars: globals().update(global_override_vars)

    # Set Project Modes
    UI_CONFIG = DictData({
        "PROJECT_MODES": MODES
    })

    # Create Sidebar
    build_sidebar_app(UI_CONFIG, globals(), show_home_page=False, sidebar_title="Choose Classification Algorithm")


#############################################################################################################################
# Repo Based Vars
PATHS = {}
DEFAULT_VIDEO_DURATION = 2.0

# Util Vars


# Util Functions


# Main Functions


# UI Functions


# Repo Based Functions
def linear_regression(**kwargs):
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
        Dataset = generate_polynomial_noisy_data_2D(
            N=USERINPUT_N, degree=USERINPUT_TrueDegree, noise_factor=USERINPUT_NoiseFactor, valRange=[-1.0, 1.0], coeffValRange=[-1.0, 1.0]
        )

        # Run Polynomial Regressions
        degrees_coeffs = []
        for i in range(USERINPUT_RegDegrees[0], USERINPUT_RegDegrees[1] + 1):
            coeffs = PolynomialRegression(Dataset["X"], Dataset["Y"], i)
            degrees_coeffs.append(coeffs)
        # Find Errors
        errors = GetErrors(Dataset["X"], Dataset["Y"], degrees_coeffs)
        best_coeffs_index = np.argmin(errors)

        # Generate and Display Classification Images
        col1, col2 = st.columns(2)
        col1.markdown("Best Fit Polynomial - Degree " + str(USERINPUT_RegDegrees[0] + best_coeffs_index))
        col2.markdown("```python\n" + DisplayPolynomial(degrees_coeffs[best_coeffs_index]))

        degrees = np.arange(USERINPUT_RegDegrees[0], USERINPUT_RegDegrees[1] + 1)
        I_regCurves, fig_regCurves = PlotRegressionCurves(
            Dataset["X"], Dataset["Y"], degrees_coeffs, 
            degrees=degrees, title="Regression Curves"
        )
        # st.image(I_regCurves, caption="Regression Curves", use_container_width=True)
        st.plotly_chart(fig_regCurves, use_container_width=True)

        I_errors, fig_errors = PlotErrors(errors, degrees, title="Degrees vs Errors")
        # st.image(I_errors, caption="Degrees vs Errors", use_container_width=True)
        st.plotly_chart(fig_errors, use_container_width=True)
    
#############################################################################################################################
# Run Code
if __name__ == "__main__":
    main()