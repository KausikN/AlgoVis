"""
Stream lit GUI for Equation Algorithms
"""

# Imports
import matplotlib.pyplot as plt

from streamlit_common_utils._common import DictData
from streamlit_common_utils.streamlit_common_ui_setup import *

from .EquationVis import *

# Main Functions
def main(selected="Equation Algorithms", MODES=[], global_override_vars=None, **kwargs):
    # Update global variables
    if global_override_vars: globals().update(global_override_vars)

    # Set Project Modes
    UI_CONFIG = DictData({
        "PROJECT_MODES": MODES
    })

    # Create Sidebar
    build_sidebar_app(UI_CONFIG, globals(), show_home_page=False, sidebar_title="Choose Equation Algorithm")


#############################################################################################################################
# Repo Based Vars
PATHS = {}
DEFAULT_VIDEO_DURATION = 2.0

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
def equation_vis(**kwargs):
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
# Run Code
if __name__ == "__main__":
    main()