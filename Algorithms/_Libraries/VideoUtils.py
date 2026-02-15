"""
Library for basic video functions
"""

# Imports
import os
import cv2
import subprocess
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from moviepy import ImageClip, concatenate_videoclips

from streamlit_common_utils.image import *
from streamlit_common_utils.video import *

# Main Functions
def Image_AddTextBox_TopLeft(I, text, textColor=[255, 255, 255]):
    '''
    Add text to an image with box at the top-left corner
    '''
    return add_text_to_image_with_box(I, text, start_left_top=(True, True), bg_color=(255,0,0))