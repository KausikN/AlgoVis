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

# Main Functions
def ReadImage(imgPath, imgSize=None, keepAspectRatio=False):
    '''
    Read an image from a given path and resize it to a given size
    '''
    I = cv2.imread(imgPath)
    if not imgSize == None:
        size_original = [I.shape[0], I.shape[1]]
        print(size_original)
        if keepAspectRatio:
            if imgSize[1] > imgSize[0]:
                imgSize = (size_original[0] * (imgSize[1] / size_original[1]), imgSize[1])
            elif imgSize[0] > imgSize[1]:
                imgSize = (imgSize[0], size_original[1] * (imgSize[0] / size_original[0]))
            else:
                if size_original[1] > size_original[0]:
                    imgSize = (size_original[0] * (imgSize[1] / size_original[1]), imgSize[1])
                else:
                    imgSize = (imgSize[0], size_original[1] * (imgSize[0] / size_original[0]))
            imgSize = (int(round(imgSize[1])), int(round(imgSize[0])))
        I = cv2.resize(I, imgSize)
    # I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    return I

def DisplayImage(I, title=""):
    '''
    Display an image with a given title
    '''
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    plt.imshow(I, "gray")
    plt.title(title)
    plt.show()

def SaveImage(I, path):
    '''
    Save an image to a given path
    '''
    cv2.imwrite(path, I)

def ReadVideo(path):
    '''
    Read a video from a given path
    '''
    cap = cv2.VideoCapture(path)
    return cap

def WebcamVideo():
    '''
    Access the webcam video feed
    '''
    return cv2.VideoCapture(0)

def SaveFrames2Video_FFMPEG(frames, pathOut, fps=20.0, size=None):
    '''
    Save a list of frames to a video file or GIF using FFMPEG
    '''
    if os.path.splitext(pathOut)[-1] == ".gif":
        frames_images = [Image.fromarray(frame) for frame in frames]
        extraFrames = []
        if len(frames_images) > 1: extraFrames = frames_images[1:]
        frames_images[0].save(pathOut, save_all=True, append_images=extraFrames, format="GIF", loop=0)
    else:
        if size is None: size = (frames[0].shape[1], frames[0].shape[0])
        codec = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(pathOut, codec, fps, size)
        for frame in frames:
            out.write(frame)
        out.release()

def SaveFrames2Video(frames, save_path, fps=24.0, size=None):
    '''
    Save a list of frames to a video file or GIF using MoviePy
    '''
    # Init
    frame_duration = 1.0 / fps
    FRAMES = []
    # Create Image Clips
    for i in range(len(frames)):
        frame_clip = ImageClip(frames[i]).with_duration(frame_duration)
        FRAMES.append(frame_clip)
    # Concatenate
    VIDEO = concatenate_videoclips(FRAMES, method="chain")
    # Write Video
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    VIDEO.write_videofile(save_path, fps=fps)

def FixVideoFile(pathIn, pathOut):
    '''
    Fix a video file by re-encoding it using FFMPEG
    '''
    COMMAND_VIDEO_CONVERT = "ffmpeg -i \"{path_in}\" -vcodec libx264 \"{path_out}\""
    
    if os.path.exists(pathOut):
        os.remove(pathOut)

    convert_cmd = COMMAND_VIDEO_CONVERT.format(path_in=pathIn, path_out=pathOut)
    print("Running Conversion Command:")
    print(convert_cmd + "\n")
    ConvertOutput = subprocess.getoutput(convert_cmd)
    print("Conversion Output: \n" + ConvertOutput + "\n")

def ImageAddText(I, text, textColor=[255, 255, 255]):
    '''
    Add text to an image at the top-left corner
    '''
    BG_COLOR = [0, 0, 0]

    I_size = I.shape[:2]
    pos = (int(I_size[1]/10), int(I_size[0]/10))

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5 * (np.max(I.shape) / 512)
    fontThickness = max(1, int(1 * (np.max(I.shape) / 512)))
    paddingScale = 0.01
    padding = [int(I.shape[0] * paddingScale), int(I.shape[1] * paddingScale)]

    text_size, _ = cv2.getTextSize(text, font, fontScale, fontThickness)
    text_w, text_h = text_size
    I_t = cv2.rectangle(I, (pos[0] - padding[0], pos[1] + padding[1]), (pos[0] + text_w + padding[0], pos[1] - text_h - padding[1]), BG_COLOR, -1)
    I_t = cv2.putText(I_t, text, pos, font, fontScale, textColor, fontThickness)
    return I_t

# Run Code
# Params

# # Params

# # RunCode