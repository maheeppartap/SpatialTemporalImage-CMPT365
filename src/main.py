import sys

from STIclass import STI
from guiCode import *


def main():
    print("Python version: " + str(sys.version))
    print("OpenCV version: " + str(cv2.__version__))

    begin()


if __name__ == "__main__":
    main()
