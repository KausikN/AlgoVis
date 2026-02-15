"""
PlotGIFLibrary is a library for generation, editing and viewing of GIFs / Videos of Plot Data
"""

# Imports
import cv2
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from streamlit_common_utils.color import *
from streamlit_common_utils.plot import *
from streamlit_common_utils.video import *

# Main Functions
# Bar Visualisations
def ListOrderPlot_Bar(listTrace, showAxis=True, figsize=(6.4, 4.8), dpi=100.0):
    '''
    List Order Plot - Visualise the ordering of a list as a bar chart animation
    '''
    fig = Figure(figsize=figsize, dpi=dpi)
    canvas = FigureCanvasAgg(fig)   

    colors = generate_rainbow_colors(len(listTrace[0]))
    orderMap = {}
    for i in range(len(listTrace[0])):
        orderMap[listTrace[-1][i]] = i

    PlotIs = []
    for i, listVals in enumerate(listTrace):
        fig.clear(True)
        ax = fig.add_subplot(111)
        if not showAxis:
            ax.axis("off")
            ax.margins(0)
            fig.tight_layout(pad=0)

        colors_ordered = [colors[orderMap[val]] for val in listVals]
        ax.bar(range(len(listVals)), listVals[:], color=colors_ordered)
        ax.title.set_text(str(i))

        canvas.draw()
        buf = canvas.buffer_rgba()
        I_effect = cv2.cvtColor(np.asarray(buf), cv2.COLOR_RGBA2RGB)
        PlotIs.append(I_effect)

    return PlotIs