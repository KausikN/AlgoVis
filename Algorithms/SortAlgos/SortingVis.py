"""
Algorithm Visualisation for Sorting Algorithms
"""

# Imports
import numpy as np
from .._Libraries import PlotAnimateLibrary as PAL
from .._Libraries import VideoUtils

# Main Functions
# Generate Array Functions
def GenerateArray_Random(size):
    inputArr = np.arange(size)
    np.random.shuffle(inputArr)
    return inputArr

# Visualiser Functions
def SortVis_PlotGIF(SortFunc, inputArr, savePath="AlgoVis/GeneratedVisualisations/SortVis_Trace.gif", duration=2.0):
    # print("Input Array:", inputArr)
    sortedArr, trace = SortFunc(inputArr)
    # print("Swaps:", len(trace))
    # print("Sorted Array:", sortedArr)
    
    PlotIs = PAL.ListOrderPlot_Bar(trace)

    padding = 5
    PlotIs = [PlotIs[0]] * padding + PlotIs + [PlotIs[-1]] * padding

    PAL.SaveImages2GIF(PlotIs, savePath, fps=len(PlotIs)/duration)

    return sortedArr, trace

# Sort Functions
def Sort_InsertionSort(inputArr):
    """
    Insertion Sort
    """
    sortedArr = list(inputArr)
    trace = []
    for i in range(1, len(sortedArr)):
        j = i
        while j > 0 and sortedArr[j-1] > sortedArr[j]:
            sortedArr[j], sortedArr[j-1] = sortedArr[j-1], sortedArr[j]
            trace.append(list(np.copy(sortedArr)))
            j -= 1
    return sortedArr, trace

def Sort_BubbleSort(inputArr):
    """
    Bubble Sort
    """
    sortedArr = list(inputArr)
    trace = []
    for i in range(len(sortedArr)):
        for j in range(i, len(sortedArr)):
            if sortedArr[j] < sortedArr[i]:
                sortedArr[i], sortedArr[j] = sortedArr[j], sortedArr[i]
                trace.append(list(np.copy(sortedArr)))
    return sortedArr, trace

def Sort_SelectionSort(inputArr):
    """
    Selection Sort
    """
    sortedArr = list(inputArr)
    trace = []
    for i in range(len(sortedArr)):
        minIndex = i
        for j in range(i, len(sortedArr)):
            if sortedArr[j] < sortedArr[minIndex]:
                minIndex = j
        sortedArr[i], sortedArr[minIndex] = sortedArr[minIndex], sortedArr[i]
        trace.append(list(np.copy(sortedArr)))
    return sortedArr, trace

def Sort_MergeSort(inputArr):
    """
    Merge Sort
    """
    sortedArr = list(inputArr)
    trace = []
    if len(sortedArr) <= 1:
        return sortedArr, [[sortedArr[0]]]
    mid = len(sortedArr) // 2
    leftArr = sortedArr[:mid]
    rightArr = sortedArr[mid:]

    leftSortedArr, leftTrace = Sort_MergeSort(leftArr)
    rightSortedArr, rightTrace = Sort_MergeSort(rightArr)

    leftIndex = 0
    rightIndex = 0
    while leftIndex < (len(leftTrace)-1) or rightIndex < (len(rightTrace)-1):
        trace.append(leftTrace[leftIndex] + rightTrace[rightIndex])
        leftIndex = min(leftIndex+1, len(leftTrace)-1)
        rightIndex = min(rightIndex+1, len(rightTrace)-1)
    
    i = 0
    j = 0
    k = 0
    sortedArr = leftSortedArr + rightSortedArr
    while i < len(leftSortedArr) and j < len(rightSortedArr):
        if leftSortedArr[i] < rightSortedArr[j]:
            # sortedArr[i] = sortedArr[k]
            sortedArr[k] = leftSortedArr[i]
            i += 1
        else:
            # sortedArr[mid + j] = sortedArr[k]
            sortedArr[k] = rightSortedArr[j]
            j += 1
        k += 1
        trace.append(list(np.copy(sortedArr)))
    while i < len(leftSortedArr):
        # sortedArr[i] = sortedArr[k]
        sortedArr[k] = leftSortedArr[i]
        i += 1
        k += 1
        trace.append(list(np.copy(sortedArr)))
    while j < len(rightSortedArr):
        # sortedArr[mid + j] = sortedArr[k]
        sortedArr[k] = rightSortedArr[j]
        j += 1
        k += 1
        trace.append(list(np.copy(sortedArr)))
    return sortedArr, trace

def Sort_QuickSort(inputArr): # TODO: Fix
    """
    Quick Sort
    """
    sortedArr = list(inputArr)
    trace = []
    if len(sortedArr) == 1:
        return sortedArr, [[sortedArr[0]]]
    elif len(sortedArr) < 1:
        return sortedArr, [[]]
    pivot = sortedArr[0]
    leftArr = []
    rightArr = []
    for i in range(1, len(sortedArr)):
        if sortedArr[i] < pivot:
            leftArr.append(sortedArr[i])
        else:
            rightArr.append(sortedArr[i])
    leftSortedArr, leftTrace = Sort_QuickSort(leftArr)
    rightSortedArr, rightTrace = Sort_QuickSort(rightArr)

    leftIndex = 0
    rightIndex = 0
    while leftIndex < (len(leftTrace)-1) or rightIndex < (len(rightTrace)-1):
        trace.append(leftTrace[leftIndex] + rightTrace[rightIndex])
        leftIndex = min(leftIndex+1, len(leftTrace)-1)
        rightIndex = min(rightIndex+1, len(rightTrace)-1)
    
    i = 0
    j = 0
    k = 0
    while i < len(leftSortedArr) and j < len(rightSortedArr):
        if leftSortedArr[i] < rightSortedArr[j]:
            # sortedArr[i] = sortedArr[k]
            sortedArr[k] = leftSortedArr[i]
            i += 1
        else:
            # sortedArr[mid + j] = sortedArr[k]
            sortedArr[k] = rightSortedArr[j]
            j += 1
        k += 1
        trace.append(list(np.copy(sortedArr)))
    while i < len(leftSortedArr):
        # sortedArr[i] = sortedArr[k]
        sortedArr[k] = leftSortedArr[i]
        i += 1
        k += 1
        trace.append(list(np.copy(sortedArr)))
    while j < len(rightSortedArr):
        # sortedArr[mid + j] = sortedArr[k]
        sortedArr[k] = rightSortedArr[j]
        j += 1
        k += 1
        trace.append(list(np.copy(sortedArr)))

    return sortedArr, trace

# Main Vars
SORT_ALGORITHMS = {
    "Bubble Sort": Sort_BubbleSort,
    "Insertion Sort": Sort_InsertionSort,
    "Selection Sort": Sort_SelectionSort,
    "2-Way Merge Sort": Sort_MergeSort
}

# Driver Code