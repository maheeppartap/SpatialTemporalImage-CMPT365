"""
    This class is for making transitions more noticable in video
    It will take a list of transitions, and video, and ouput a

"""
import cv2

from src.transitions import Transition
from src.videoSpecs import VideoSpecs
from src.transitions import ColWipe
from src.transitions import EmptyTrans


#: :type: list of Transition
def enhance(filename: str, transitions: list, outfile=None):
    # this is probably done, but just to make sure
    # sort transitions
    transitions = sorted(transitions)

    if not outfile:
        outfile = outputfile(filename)

    vidCapture = cv2.VideoCapture(filename)
    # Check if camera opened successfully
    if not vidCapture.isOpened():
        print("Error opening video  file")

    width = int(vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidCapture.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # set video properties for all the transitions to use
    Transition.vidspec = VideoSpecs(width, height, length, fps)

    out = cv2.VideoWriter(outfile, fourcc, fps, (width, height))

    # for testing purposes
    transitions.append(ColWipe(35, 76, 0, 1))
    i = 0
    index = 0

    transitions.append(EmptyTrans())

    while vidCapture.isOpened():
        # Capture frame-by-frame
        ret, frame = vidCapture.read()
        if ret:
            if transitions[i].draw_on_frame(frame, index):
                i += 1
            # this just copies the whole file to the ouput destination
            out.write(frame)
            index += 1
        else:
            break

    vidCapture.release()
    out.release()
    # just to be safe


# TODO: implement this
def outputfile(filename):
    split = filename.split(".")
    return split[0] + "_enhanced.mp4"
