# returns a list of transitions
import math
import os

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
def _detect_lines(sti) -> list:
    lines = _simple_line_detection(sti)
    groups = _first_pass_group(lines)
    lines = _combine_lines(groups)
    _weed_false_positives(lines)
    _extrapolate_end_points(lines)
    return lines


# use openCV to find simple lines
def _simple_line_detection(sti) -> list:
    pass


# group the lines into groups based on how close they are, order by first point
# returns list of groups, (where a group is a list of lines that are close)
def _first_pass_group(lines) -> list:
    pass


# ALL combine_lines have the same input and output, just different methods of achieving
# this is just an easy way to toggle between them and see which is better
# maybe later we will make the combiner a toggle
def _combine_lines(groups) -> list:
    return _combine_lines_thresholded(groups)


# check each group to see if any of the lines can be combined, return list of lines
def _combine_lines_regression(groups) -> list:
    pass


# feel free to add another method
def _combine_lines_hypothesis(groups) -> list:
    pass


def _combine_lines_thresholded(groups) -> list:
    pass


# remove any lines that appear to be false positives
def _weed_false_positives(lines) -> None:
    pass


# make the end points be 0 or 1, instead of somewhere in the middle
def _extrapolate_end_points(lines) -> None:
    pass

# simple as it sounds
def _map_lines_to_transitions(lines, type) -> list:
    pass


def analyze_sti(img, c, filename):
    detectedSTItransition = np.zeros(2, dtype="float")
    cv2.imwrite("temp.png", img)
    img = cv2.imread("temp.png")
    gray = img.copy()

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    low_threshold = 20
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    height, width, channels = img.shape
    rho = 1
    theta = np.pi / 180
    threshold = 10  # seems like a sweet spot
    min_line_length = 20
    max_line_gap = 2
    line_image = np.copy(img) * 0

    lines_ = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                             min_line_length, max_line_gap)

    lines = np.copy(lines_)

    k = 0
    slope = np.zeros(len(lines))
    # print(self.detectedSTItransition)
    if type(lines) is np.ndarray:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        print(lines)

        lines = enhanceImg(lines)

        print("now: ", lines)
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

        cv2.imshow("detected transition", lines_edges)
    else:
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
        cv2.imshow("detected transition", lines_edges)

    os.remove("temp.png")
    k = 0
    for line in lines:
        showTransition(line[0], filename)
        typeOfTransition(x=slope[k], c=c, timeline=lines[0])
        k += 1
    cv2.waitKey(0)


def typeOfTransition(c, x, timeline=0):
    if x is 0:
        return
    type = ""

    print("slope is: ", x)
    theta = math.atan(x)
    print(theta)
    if theta > 0:
        if c:
            # tempTransition = ColWipe(start=timeline[0], end=timeline[2], scol=timeline[1], ecol=timeline[2])
            type = "lr"
        else:
            # tempTransition = HorWipe(start=timeline[1], end=timeline[0], srow=timeline[4], erow=timeline[3])
            type = "ud"
    else:
        if theta < 0:
            if c:
                # tempTransition = ColWipe(start=timeline[0], end=timeline[2], scol=timeline[1], ecol=timeline[2])
                type = "rl"
            else:
                # tempTransition = HorWipe(start=timeline[1], end=timeline[0], srow=timeline[4], erow=timeline[3])
                type = "du"
    # self.listOfTransitions.append(tempTransition)
    print("type is: ", type)
    print("done")


def showTransition(x, filename):
    cap = cv2.VideoCapture(filename)
    cap.set(1, x[0])
    ret, beginFrame = cap.read()
    cv2.imshow("dvjwhevdu", beginFrame)

    cap.set(1, int((x[0] + x[2]) / 2))
    ret, middleFrame = cap.read()

    cap.set(1, x[2])
    ret, endFrame = cap.read()
    cap.release()


def enhanceImg(lines):
    xInterceptTol = 50
    slopeTol = 1
    index = []
    lines_ = np.copy(lines)
    index = []
    for line in lines:
        lines_ = np.delete(lines_, 0, 0)
        slope = float((line[0][3] - line[0][1]) / (line[0][2] - line[0][0]))
        xIntercept = float((-1) * slope * line[0][0])
        k = 0
        for cmp in lines_:
            k += 1
            slope_ = float((cmp[0][3] - cmp[0][1]) / (cmp[0][2] - cmp[0][0]))
            xIntercept_ = float((-1) * slope_ * cmp[0][0])
            if abs(slope_ - slope) > slopeTol:
                # print("line is: ", lines, " cmp is: ", cmp, " slope diff: ", abs(slope_-slope))
                continue
            if abs(xIntercept_ - xIntercept) > xInterceptTol:
                # print("line is: ", lines, " cmp is: ", cmp, " intercept diff: ", abs(xIntercept_ - xIntercept))
                continue
            index.append(k)
            line[0][2] = cmp[0][2]
            line[0][3] = cmp[0][3]

    lines = np.delete(lines, index, 0)
    print("Lines is now: ", lines)

    # np.delete(lines, index, 1)
    print(lines)
    print("index is: ", index)
    return lines
