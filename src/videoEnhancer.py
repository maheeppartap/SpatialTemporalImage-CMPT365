"""
    This class is for making transitions more noticable in video
    It will take a list of transitions, and video, and ouput a

"""
import cv2

from transitions import *
from videoSpecs import VideoSpecs
from randomColourGen import *


#: :type: list of Transition
def enhance(filename: str, transitions: list, outfile: str, resolution=720, typeCol='n'):
    vidCapture = cv2.VideoCapture(filename)
    # Check if camera opened successfully
    if not vidCapture.isOpened():
        print("Error opening video file!")

    width = int(vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if height > resolution:
        print("video input resolution: " + str(height) + " is higher than output video " + str(resolution))
        print("If you wish to maintain video quality use flag -r --resolution to increase output resolution.")
        width = int(width * (resolution / height))
        height = resolution
    length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidCapture.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # set video properties for all the transitions to use
    Transition.vidspec = VideoSpecs(width, height, length, fps)

    out = cv2.VideoWriter(outfile, fourcc, fps, (width, height))

    # for testing purposes
    i = 0
    index = 0
    # adding colors to transitions

    for trans in transitions:
        r, g, b = color().retCol(typeCol)
        trans.set_rgb(r, g, b)
    # make sure starts and ends are computed
    for trans in transitions:
        trans.compute_statics()
    # sort by starts and ends
    transitions = sorted(transitions)
    # add an empty transition at the end to avoid index out of bound error
    transitions.append(EmptyTrans())

    while vidCapture.isOpened():
        # Capture frame-by-frame
        ret, frame_full = vidCapture.read()
        if ret:
            frame = cv2.resize(frame_full, (width, height))
            if transitions[i].draw_on_frame(frame, index):
                while transitions[i].start <= index:
                    i += 1
            # this just copies the whole file to the ouput destination
            out.write(frame)
            index += 1
        else:
            break

    vidCapture.release()
    out.release()
    # just to be safe
