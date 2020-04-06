"""
    This class is for making transitions more noticable in video
    It will take a list of transitions, and video, and ouput a

"""
import cv2

from src.transitions import Transition
from src.videoSpecs import VideoSpecs


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

    width = vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    length = vidCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vidCapture.get(cv2.CAP_PROP_FPS)
    # set video properties for all the transitions to use
    Transition.vidspec = VideoSpecs(width, height, length, fps)
    out = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))

    while vidCapture.isOpened():
        # Capture frame-by-frame
        ret, frame = vidCapture.read()
        if ret:
            # this just copies the whole file to the ouput destination
            out.write(frame)
        else:
            break

    vidCapture.release()
    out.release()
    # just to be safe
    cv2.destroyAllWindows()

#TODO: implement this
def outputfile(filename):
    return "hello"
