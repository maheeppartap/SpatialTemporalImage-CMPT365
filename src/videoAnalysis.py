import cv2
import numpy as np
import math
import os
from matplotlib import pyplot as plt


class VideoAnalysis:

    def __init__(self, filename, thresh=0.7, size=64):
        self.filename = filename
        self.thresh = thresh
        self.width = -1
        self.height = size
        self.length = -1
        self.rowsti = None
        self.colsti = None

    def analyse(self, complete_callback=None):
        self.breakdowntoSTI()
        if complete_callback:
            complete_callback(self)

    def breakdowntoSTI(self):
        vidCapture = cv2.VideoCapture(self.filename)
        # Check if camera opened successfully
        if not vidCapture.isOpened():
            print("Error opening video  file")

        width = vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # reduce the size
        width = int(width / (height / self.height))
        height = self.height

        length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = width
        self.length = length

        index = 0
        N = int(1 + np.log2(height))

        prevcolhists = np.full((width, N, N), width + 1, dtype=int)
        prevrowhists = np.full((height, N, N), height + 1, dtype=int)
        colhists = np.zeros((width, N, N), int)
        rowhists = np.zeros((height, N, N), int)
        self.colsti = np.empty((width, length), dtype=np.uint8)
        self.rowsti = np.empty((height, length), dtype=np.uint8)
        # Read until video is completed
        while vidCapture.isOpened():

            # Capture frame-by-frame
            ret, frame_full = vidCapture.read()

            if ret:
                # reduce resolution
                frame = cv2.resize(frame_full, (width, height))
                # create a histogram for every row and column in the given frame
                for i in range(height):
                    for j in range(width):
                        # convert to chromaticity
                        total = np.sum(frame[i][j])
                        if total == 0:
                            r = 0
                            g = 0
                        else:
                            r = frame[i][j][0] / total
                            g = frame[i][j][1] / total
                        # quantize chromaticity
                        rN = int(np.floor(r * (N - 1)))
                        gN = int(np.floor(g * (N - 1)))
                        if rN == 7 or gN == 7:
                            pass
                        #   print(str(frame[i][j]))
                        #  print(str(r) + " " + str(g))
                        colhists[j][rN][gN] += 1
                        rowhists[i][rN][gN] += 1

                # create a column of our column sti
                for i in range(width):
                    diff = self.hist_intersection(height, N, prevcolhists[i], colhists[i])
                    self.colsti[i][index] = (diff > self.thresh) * 255

                for i in range(height):
                    diff = self.hist_intersection(width, N, prevrowhists[i], rowhists[i])
                    self.rowsti[i][index] = (diff > self.thresh) * 255

                index += 1
                # Display the resulting frame
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            # Break the loop
            else:
                break
        # display()
        vidCapture.release()
        cv2.destroyAllWindows()  # just to be safe

    # VERY IMPORTANT, this function also resets the histogram for next loop
    # NOT SAFE
    @staticmethod
    def hist_intersection(total, N, prevhist, hist):
        diff = 0
        for j in range(N):
            for k in range(N):
                diff += min(prevhist[j][k], hist[j][k])
                # reset for next loop since we are done with it
                prevhist[j][k] = hist[j][k]
                hist[j][k] = 0
        diff /= total
        return diff

    @staticmethod
    def ibm_hist_diff(total, N, prevhist, hist):
        pass

    def analyze_sti(self, c):
        if c:
            img = self.colsti
        else:
            img = self.rowsti

        self.detectedSTItransition = np.zeros(2, dtype="float")
        cv2.imwrite("temp.png", img)
        img = cv2.imread("temp.png")
        gray = img.copy()

        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        low_threshold = 50
        high_threshold = 150
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
        height, width, channels = img.shape
        rho = 1
        theta = np.pi / 180
        threshold = 20  # seems like a sweet spot
        min_line_length = 0.9*height
        max_line_gap = 2
        line_image = np.copy(img) * 0

        lines_ = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                                 min_line_length, max_line_gap)

        lines = np.copy(lines_)

        k = 0
        slope = np.zeros(len(lines))
        length = np.zeros(len(lines))
        if type(lines) is np.ndarray:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    slope[k] = float((y2 - y1) / (x2 - x1))
                    length[k] = math.hypot(x1 - x2, y1 - y2)
                    self.detectedSTItransition[k] = lines[len(lines) - 1][0][0]
                    self.detectedSTItransition[k+1] = lines[len(lines) - 1][0][2]
                    k += 1

        print(self.detectedSTItransition)
        if type(lines) is np.ndarray:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

            print(lines)

            self.lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
            cv2.imshow("detected transition", self.lines_edges)
        else:
            self.lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
            cv2.imshow("detected transition", self.lines_edges)

        os.remove("temp.png")
        for line in lines:
            self.showTransition(x=line[0])

        self.typeOfTransition(x = slope, c = c)

        cv2.waitKey(0)

    def typeOfTransition(self, c, x):
        if x is 0:
            return
        type = ""
        for slope in x:
            print("slope is: ", slope)
            theta = math.atan(slope)
            print(theta)
            if theta > 0:
                if c:
                    type = "lr"
                else:
                    type = "ud"
            else:
                if theta < 0:
                    if c:
                        type = "rl"
                    else:
                        type = "du"

        print("type is: ", type)


    def showTransition(self, x):
        cap = cv2.VideoCapture(self.filename)
        cap.set(1, x[0])
        ret, self.beginFrame = cap.read()

        cap.set(1,int((x[0]+x[2])/2))
        ret, self.middleFrame = cap.read()

        cap.set(1, x[2])
        ret, self.endFrame = cap.read()
        cap.release()








