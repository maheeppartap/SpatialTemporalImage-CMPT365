import os
import sys
from time import time

from src.videoAnalysis import VideoAnalysis
from src.videoEnhancer import enhance
from src.videoBreakdown import breakdowntoSTI


def main():
    outfile = None
    args = sys.argv
    filepath = args[1]
    if len(args) >= 3:
        outfile = args[2]
    # va = VideoAnalysis(filepath)
    # va.analyse()
    filepath = get_full_name(filepath)
    start = time()
    breakdowntoSTI(filepath)
    end = time()
    print(end-start)
    # enhance(filepath, [], outfile)


def get_full_name(filename):
    if not os.path.isfile(filename):
        raise ValueError(filename + " doesn't exist!")
    else:
        return os.path.abspath(filename)

if __name__ == "__main__":
    main()