"""
Maze Generator
"""

# Imports
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Main Functions
# Visualisation Functions
def VisualiseCellMatrix(cell_matrix, image_scale=10, bg_color=[0, 0, 0], line_color=[255, 255, 0], line_thickness=1, display=True):
    '''
    Visualises a cell matrix
    '''
    # Init Colors
    bg_color = np.array(bg_color, dtype=np.uint8)
    line_color = tuple(line_color)

    # Initialise Image
    I = np.ones((cell_matrix.shape[0] * image_scale, cell_matrix.shape[1] * image_scale, 3), np.uint8) * bg_color
    # Draw lines
    for i in range(cell_matrix.shape[0]):
        for j in range(cell_matrix.shape[1]):
            if cell_matrix[i][j][0]:
                cv2.line(I, (j * image_scale, i * image_scale), (j * image_scale, (i * image_scale) + image_scale), 
                    line_color, line_thickness)
            if cell_matrix[i][j][1]:
                cv2.line(I, (j * image_scale, i * image_scale), ((j * image_scale) + image_scale, i * image_scale), 
                    line_color, line_thickness)
            if cell_matrix[i][j][2]:
                cv2.line(I, ((j * image_scale) + image_scale, i * image_scale), 
                    ((j * image_scale) + image_scale, (i * image_scale) + image_scale), 
                    line_color, line_thickness)
            if cell_matrix[i][j][3]:
                cv2.line(I, (j * image_scale, (i * image_scale) + image_scale), 
                    ((j * image_scale) + image_scale, (i * image_scale) + image_scale), 
                    line_color, line_thickness)
    
    # Show image
    if display:
        plt.title("Maze")
        plt.imshow(I)
        plt.show()

    return I

# Generator Functions
def GenerateCell_Random():
    '''
    Generates a random cell with 4 binary values
    Each binary value represents whether to draw a line in North, East, South, or West direction
    '''
    # Generate binary for each direction
    cell = np.random.randint(0, 2, 4, dtype=bool)
    return cell

def GenerateCellMatrix_Random(size):
    '''
    Generates a random cell matrix with given size
    '''
    # Generate random cell matrix
    cell_matrix = np.random.randint(0, 2, (size[0], size[1], 4), dtype=bool)
    return cell_matrix

# Driver Code
# Params
size = (10, 10)


savePath = "GeneratedVisualisations/GeneratedMaze.png"

display = True
save = False
# Params

# RunCode
# Generate Maze
cell_matrix = GenerateCellMatrix_Random(size)

# Visualise Maze
I_Maze = VisualiseCellMatrix(cell_matrix, display=display)

# Save Maze Image
if save:
    cv2.imwrite(savePath, I_Maze)