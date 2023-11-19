"""
Stream lit GUI for hosting AlgoVis
"""

# Imports
import os
import cv2
import json
import functools
import subprocess
import numpy as np
import streamlit as st

# Main Vars
config = json.load(open("./StreamLitGUI/UIConfig.json", "r"))
config_subapp = {}

# Main Functions
def main():
    global DEFAULT_VIDEO_DURATION
    global config
    global config_subapp

    # Set Project Modes
    config["PROJECT_MODES"] = [p["APP_NAME"] for p in config["SUB_APPS"]]

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose one of the following",
        tuple(
            [config["PROJECT_NAME"]] + 
            config["PROJECT_MODES"]
        )
    )
    DEFAULT_VIDEO_DURATION = st.sidebar.slider("Generated Video Duration", 0.1, 5.0, 2.0, 0.1)
    
    if selected_box == config["PROJECT_NAME"]:
        HomePage()
    else:
        # Run SubApp
        subAppIndex = config["PROJECT_MODES"].index(selected_box)
        config_subapp = config["SUB_APPS"][subAppIndex]
        RunSubApp(PATHS["sub_apps"] + config["SUB_APPS"][subAppIndex]["FILE_NAME"] + ".py")
        # correspondingFuncName = selected_box.replace(" ", "_").lower()
        # if correspondingFuncName in globals().keys():
        #     globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config["PROJECT_NAME"])
    st.markdown("Github Repo: " + "[" + config["PROJECT_LINK"] + "](" + config["PROJECT_LINK"] + ")")
    st.markdown(config["PROJECT_DESC"])

    # st.write(open(config["PROJECT_README"], "r").read())

#############################################################################################################################
# Repo Based Vars
PATHS = {
    "sub_apps": "StreamLitGUI/apps/",
    "default": {
        "save": {
            "gif": "StreamLitGUI/DefaultData/SavedGIF.gif",
            "video": "StreamLitGUI/DefaultData/SavedVideo.avi",
            "video_converted": "StreamLitGUI/DefaultData/SavedVideo_Converted.mp4"
        }
    }
}
DEFAULT_VIDEO_DURATION = 2.0

# Util Vars


# Util Functions
def RunSubApp(path):
    if os.path.exists(path):
        exec(open(path, "r").read(), globals())

def RunAllSubApps(dir_path):
    for f in os.listdir(dir_path):
        if f.endswith(".py"):
            # print("Running SubApp: " + f)
            RunSubApp(os.path.join(dir_path, f))

def GetFunctionsByPrefixName(module, prefixName):
    fnames = [x for x in dir(module) if x.startswith(prefixName)]
    funcs = {}
    for f in fnames:
        funcs[f] = getattr(module, f)
    return funcs

def GetNames(data):
    return [x["name"] for x in data.keys()]

# Main Functions


# UI Functions


# Repo Based Functions
# # Run All Sub Apps
# RunAllSubApps(PATHS["sub_apps"])

# Custom Apps
def search_algorithms():
    # Title
    st.header("Search Algorithms")

    st.markdown("In Developement :stuck_out_tongue_winking_eye:")

#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()