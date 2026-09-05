"""
Stream lit GUI for hosting AlgoVis
"""

# Imports
from streamlit_common_utils._common import DictData
from streamlit_common_utils.streamlit_common_ui_setup import *

from AlgoVis import *

# Main Vars
UI_CONFIG = UIConfig("./StreamLitGUI/UIConfig.json")
UI_DATA = UIData("./StreamLitGUI/UIData.json")
UI_CACHE = UICache(UI_DATA.get("paths.cache"))

# Main Functions
def main():
    global DEFAULT_VIDEO_DURATION

    # Set Project Modes
    UI_CONFIG.set("PROJECT_MODES", [UI_CONFIG.get(f"SUB_APPS.{key}.APP_NAME") for key in UI_CONFIG.get("SUB_APPS", {})])

    # Params
    DEFAULT_VIDEO_DURATION = st.sidebar.slider("Generated Video Duration", 0.1, 5.0, 2.0, 0.1)

    # Create Sidebar
    build_sidebar_app(
        UI_CONFIG, SUBAPPS,
        common_args={
            "global_override_vars": {
                "PATHS": UI_DATA.get("paths"),
                "DEFAULT_VIDEO_DURATION": DEFAULT_VIDEO_DURATION
            }
        },
        page_funcs_args=UI_CONFIG.get("SUB_APPS"),
        sidebar_title="Choose Sub App"
    )


#############################################################################################################################
# Repo Based Vars
DEFAULT_VIDEO_DURATION = 2.0

# Util Vars


# Util Functions


# Main Functions


# UI Functions


# Repo Based Functions

# Custom Apps


#############################################################################################################################
# Run Code
if __name__ == "__main__":
    main()