# returns a list of transitions
import math
import os

from transitions import *
import cv2
import numpy as np


# main function for command line
def detect_transitions(colsti, rowsti) -> list:
    # detect the lines
    col_lines = _detect_lines(colsti)
    row_lines = _detect_lines(rowsti)
    # classify them as transitions
    transitions = _map_lines_to_transitions(col_lines, True)
    transitions += _map_lines_to_transitions(row_lines, False)
    return transitions


# detect high quality lines
#type = true for col, false for row
def _detect_lines(sti) -> list:
    lines, height = _simple_line_detection(sti)
    groups = _first_pass_group(lines)
    lines = _combine_lines(groups)
    _weed_false_positives(lines, height)
    _extrapolate_end_points(lines)
    return lines


# use openCV to find simple lines
def _simple_line_detection(sti) -> (list, int):
    cv2.imwrite("temp.png", sti)    # doing this changes it to the correct format
    img = cv2.imread("temp.png")
    gray = img.copy()
    kernel_size = 5 # for a 5x5 gaussian matrix for more blur, change to 3 for less blur
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    low_threshold = 20
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    height, width, channels = img.shape
    rho = 1
    theta = np.pi / 180
    threshold = int(0.4*height)  # seems like a sweet spot
    min_line_length = 20
    max_line_gap = 2
    lines_ = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                             min_line_length, max_line_gap)
    if type(lines_) is np.ndarray:
        return list(lines_), height
    print("No transition found")
    exit(1) #exit if no transitions


# group the lines into groups based on how close they are, order by first point
# returns list of groups, (where a group is a list of lines that are close)
def _first_pass_group(lines) -> list:
    xInterceptTol = 20
    slopeTol = 1
    lines_ = np.copy(lines)
    groups = []
# comparing the lines with with all others
    for line in lines[:]:
        lines_ = np.delete(lines_, 0, 0)    #making sure the checks are not repeated,
        slope = float((line[0][3] - line[0][1]) / (line[0][2] - line[0][0]))
        b = float(line[0][1] - (slope * line[0][0])) # b from y= mx + b
        xIntercept = float((-1 * b) / slope)
        k = -1
        groups_ = [line[0]]
        for cmp in lines_:
            k += 1
            slope_ = float((cmp[0][3] - cmp[0][1]) / (cmp[0][2] - cmp[0][0]))
            b_ = float(cmp[0][1]-(slope_*cmp[0][0]))
            xIntercept_ = float((-1*b_)/slope_) #compute the intercept
            if abs(slope_ - slope) > slopeTol:
                continue
            if abs(xIntercept_ - xIntercept) > xInterceptTol:
                continue
            groups_.append(cmp[0])  #append if tests pass
        groups.append(groups_)

    return groups



# ALL combine_lines have the same input and output, just different methods of achieving
# # this is just an easy way to toggle between them and see which is better
# # maybe later we will make the combiner a toggle
def _combine_lines(groups) -> list:
    return _combine_lines_thresholded(groups)


# check each group to see if any of the lines can be combined, return list of lines
def _combine_lines_regression(groups) -> list:
    pass


# feel free to add another method
def _combine_lines_hypothesis(groups) -> list:
    pass

#sort the groups by y2 and combine them
def _combine_lines_thresholded(groups ) -> list:

    finallist = []
    for group in groups:
        group = sorted(group, key=lambda x: x[3], reverse=True)
        temp = [group[0][0], group[0][1], group[-1][2], group[-1][3]]
        finallist.append(temp)
    return finallist

# remove any lines that appear to be false positives
def _weed_false_positives(lines, height) -> list:
    threshConst = 0.7
    Threshold = threshConst*height
    finalList = []

    for line in lines:
        dist = float(math.sqrt((line[2]-line[0])*(line[2]-line[0]) - (line[3]-line[1])*(line[3]-line[1])))
        if dist > Threshold:
            finalList.append(line)

    return finalList


# make the end points be 0 or 1, instead of somewhere in the middle
def _extrapolate_end_points(lines) -> None:
    pass

# simple as it sounds
def _map_lines_to_transitions(lines, col) -> list:
    transitionList = []
    for line in lines:
        x = float((line[3] - line[1])/(line[2]-line[0]))
        b=float(line[1] - (x*line[0]))
        intercept = int((-1*b)/x)
        theta = math.atan(x)    # slope is tan(theta), so calculate theta and see if its positive or neg
        print("Theta is", theta)
        if theta > 0:
            if col:
                transitionList.append(ColWipe(start= line[0], end=intercept,scol=1, ecol=0))
            else:
                transitionList.append(HorWipe(start= intercept, end=line[2],srow=1, erow=0))
        else:
            if theta < 0:
                if col:
                    transitionList.append(ColWipe(start=intercept, end=line[2], scol=0, ecol=1))
                else:
                    transitionList.append(HorWipe(start=line[0], end=intercept, srow=0, erow=1))
    # self.listOfTransitions.append(tempTransition)
    print("list of transitions: ", transitionList)
    return transitionList

#
# def analyze_sti(img, c):
#     cv2.imwrite("temp.png", img)
#     img = cv2.imread("temp.png")
#     gray = img.copy()
#
#     kernel_size = 5
#     blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
#     low_threshold = 20
#     high_threshold = 150
#     edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
#     height, width, channels = img.shape
#     rho = 1
#     theta = np.pi / 180
#     threshold = 10  # seems like a sweet spot
#     min_line_length = 20
#     max_line_gap = 2
#     line_image = np.copy(img) * 0
#
#     lines_ = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
#                              min_line_length, max_line_gap)
#
#     lines = np.copy(lines_)
#
#     k = 0
#     slope = np.zeros(len(lines))
#     if type(lines) is np.ndarray:
#         for line in lines:
#             for x1, y1, x2, y2 in line:
#                 cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
#
#
#         lines = enhanceImg(lines)
#
#         lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
#
#         cv2.imshow("detected transition", lines_edges)
#     else:
#         lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
#         cv2.imshow("detected transition", lines_edges)
#
#     os.remove("temp.png")
#     k = 0
#     for line in lines:
#         typeOfTransition(x=slope[k], c=c, timeline=lines[0])
#         k += 1
#     cv2.waitKey(0)
#
#
# def typeOfTransition(c, x, timeline=0):
#     if x is 0:
#         return
#     type = ""
#
#     theta = math.atan(x)
#     if theta > 0:
#         if c:
#             # tempTransition = ColWipe(start=timeline[0], end=timeline[2], scol=timeline[1], ecol=timeline[2])
#             type = "lr"
#         else:
#             # tempTransition = HorWipe(start=timeline[1], end=timeline[0], srow=timeline[4], erow=timeline[3])
#             type = "ud"
#     else:
#         if theta < 0:
#             if c:
#                 # tempTransition = ColWipe(start=timeline[0], end=timeline[2], scol=timeline[1], ecol=timeline[2])
#                 type = "rl"
#             else:
#                 # tempTransition = HorWipe(start=timeline[1], end=timeline[0], srow=timeline[4], erow=timeline[3])
#                 type = "du"
#     # self.listOfTransitions.append(tempTransition)
#     print("type is: ", type)
#     print("done")
#
#
# def showTransition(x, filename):
#     cap = cv2.VideoCapture(filename)
#     cap.set(1, x[0])
#     ret, beginFrame = cap.read()
#     cv2.imshow("Begin transition", beginFrame)
#
#     cap.set(1, int((x[0] + x[2]) / 2))
#     ret, middleFrame = cap.read()
#
#     cap.set(1, x[2])
#     ret, endFrame = cap.read()
#     cap.release()
#
#
# def enhanceImg(lines):
#     xInterceptTol = 50
#     slopeTol = 1
#     index = []
#     lines_ = np.copy(lines)
#     index = []
#     for line in lines:
#         lines_ = np.delete(lines_, 0, 0)
#         slope = float((line[0][3] - line[0][1]) / (line[0][2] - line[0][0]))
#         xIntercept = float((-1) * slope * line[0][0])
#         k = 0
#         for cmp in lines_:
#             k += 1
#             slope_ = float((cmp[0][3] - cmp[0][1]) / (cmp[0][2] - cmp[0][0]))
#             xIntercept_ = float((-1) * slope_ * cmp[0][0])
#             if abs(slope_ - slope) > slopeTol:
#                 continue
#             if abs(xIntercept_ - xIntercept) > xInterceptTol:
#                 continue
#             index.append(k)
#             line[0][2] = cmp[0][2]
#             line[0][3] = cmp[0][3]
#
#     lines = np.delete(lines, index, 0)
#
#     # np.delete(lines, index, 1)
#     return lines
