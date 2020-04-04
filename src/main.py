import sys

from src.guiCode import *


# Conor in case it doesn't compile, run this through your cmd:      python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
# then this:    python -m pip install kivy.deps.gstreamer

def main():
    print("Python version: " + str(sys.version))
    print("OpenCV version: " + str(cv2.__version__))
    #xx = cv2.imread("Colsti.png")
    #analyze_sti(xx)
    mainGUI().run()
    # videoBreakDown()


if __name__ == "__main__":
    main()


