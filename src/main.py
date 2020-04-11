import sys

from src.guiCode import *
from src.transitionDetector import *
from transitionDetector import *

# Conor in case it doesn't compile, run this through your cmd:      python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
# then this:    python -m pip install kivy.deps.gstreamer
from transitionDetector import _simple_line_detection


def main():
    print("Python version: " + str(sys.version))
    print("OpenCV version: " + str(cv2.__version__))

    detect_transitions(cv2.imread("../assets/testSTI/duC.png"), cv2.imread("../assets/testSTI/duR.png"))
    # mainGUI().run()
    # videoBreakDown()


if __name__ == "__main__":
    main()


