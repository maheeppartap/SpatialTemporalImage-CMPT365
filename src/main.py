import sys

import numpy as np

from STIclass import STI
from guiCode import *


# Conor in case it doesn't compile, run this through your cmd:      python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
# then this:    python -m pip install kivy.deps.gstreamer

def main():
    print("Python version: " + str(sys.version))
    print("OpenCV version: " + str(cv2.__version__))

    # x = np.array([[2, 3], [4, 5]])
    # print(x)
    # p =[[9],[8]]
    # print(p)
    # x[:,1] = np.transpose(p)
    # print(x)


    mainGUI().run()
    #videoBreakDown()


if __name__ == "__main__":
    main()


