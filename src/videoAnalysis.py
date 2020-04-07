import cv2
import numpy as np
import math
import os
from matplotlib import pyplot as plt
from src.transitions import *
import random
from src.videoBreakdown import breakdowntoSTI

class VideoAnalysis:

    def __init__(self, filename, thresh=0.7, size=64):
        self.filename = filename
        self.thresh = thresh
        self.size = size
        self.rowsti = None
        self.colsti = None
        self.listOfTransitions = list()

    def analyse(self, complete_callback=None):
        (self.colsti, self.rowsti) = breakdowntoSTI(self.filename, self.size, self.thresh)
        if complete_callback:
            complete_callback(self)


