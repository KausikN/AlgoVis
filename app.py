"""
Stream lit GUI for hosting AlgoVis
"""

# Imports
import os
import cv2
import streamlit as st
import json
import subprocess
import functools

# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    global DEFAULT_VIDEO_DURATION

    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config['PROJECT_NAME']] + 
            config['PROJECT_MODES']
        )
    )
    DEFAULT_VIDEO_DURATION = st.sidebar.slider("Generated Video Duration", 0.1, 5.0, 2.0, 0.1)
    
    if selected_box == config['PROJECT_NAME']:
        HomePage()
    else:
        # Run SubApp
        RunSubApp(SUB_APPS_PATH + config['SUB_APPS'][config['PROJECT_MODES'].index(selected_box)] + '.py')
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config['PROJECT_NAME'])
    st.markdown('Github Repo: ' + "[" + config['PROJECT_LINK'] + "](" + config['PROJECT_LINK'] + ")")
    st.markdown(config['PROJECT_DESC'])

    # st.write(open(config['PROJECT_README'], 'r').read())

#############################################################################################################################
# Repo Based Vars
SUB_APPS_PATH = 'StreamLitGUI/apps/'

DEFAULT_SAVEPATH_GIF = "StreamLitGUI/DefaultData/SavedGIF.gif"
DEFAULT_SAVEPATH_VIDEO = "StreamLitGUI/DefaultData/SavedVideo.avi"
DEFAULT_SAVEPATH_VIDEO_CONVERTED = "StreamLitGUI/DefaultData/SavedVideo_Converted.mp4"
DEFAULT_VIDEO_DURATION = 2.0

# Util Vars
COMMAND_VIDEO_CONVERT = 'ffmpeg -i \"{path_in}\" -vcodec libx264 \"{path_out}\"'

# Util Functions
def RunSubApp(path):
    if os.path.exists(path):
        exec(open(path, 'r').read(), globals())

def RunAllSubApps(dir_path):
    for f in os.listdir(dir_path):
        if f.endswith('.py'):
            # print("Running SubApp: " + f)
            RunSubApp(os.path.join(dir_path, f))

def GetFunctionsByPrefixName(module, prefixName):
    fnames = [x for x in dir(module) if x.startswith(prefixName)]
    funcs = {}
    for f in fnames:
        funcs[f] = getattr(module, f)
    return funcs

def GetNames(data):
    return [x['name'] for x in data.keys()]

def FixSavedVideoFile():
    if os.path.exists(DEFAULT_SAVEPATH_VIDEO_CONVERTED):
        os.remove(DEFAULT_SAVEPATH_VIDEO_CONVERTED)

    convert_cmd = COMMAND_VIDEO_CONVERT.format(path_in=DEFAULT_SAVEPATH_VIDEO, path_out=DEFAULT_SAVEPATH_VIDEO_CONVERTED)
    print("Running Conversion Command:")
    print(convert_cmd + "\n")
    ConvertOutput = subprocess.getoutput(convert_cmd)

# Main Functions


# UI Functions


# Repo Based Functions
# # Run All Sub Apps
# RunAllSubApps(SUB_APPS_PATH)

# Custom Apps
def search_algorithms():
    # Title
    st.header("Search Algorithms")

    st.markdown("In Developement :stuck_out_tongue_winking_eye:")

#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()