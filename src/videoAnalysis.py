import cv2
import numpy as np


class VideoAnalysis:

    def __init__(self, filename, thresh=0.7, size=64):
        self.filename = filename
        vidCapture = cv2.VideoCapture(filename)
        # Check if camera opened successfully
        if not vidCapture.isOpened():
            print("Error opening video  file")

        self.thresh = thresh
        self.width = -1
        self.height = size
        self.length = -1
        self.rowsti = None
        self.colsti = None

    def analyse(self, complete_callback):
        self.breakdowntoSTI()
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
                            print(str(frame[i][j]))
                            print(str(r) + " " + str(g))
                        colhists[j][rN][gN] += 1
                        rowhists[i][rN][gN] += 1

                # create a column of our column sti
                for i in range(width):
                    diff = self.histogram_intersection(height, N, prevcolhists[i], colhists[i])
                    self.colsti[i][index] = (diff > self.thresh) * 255

                for i in range(height):
                    diff = self.histogram_intersection(width, N, prevrowhists[i], rowhists[i])
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
    def histogram_intersection(total, N, prevhist, hist):
        diff = 0
        for j in range(N):
            for k in range(N):
                diff += min(prevhist[j][k], hist[j][k])
                # reset for next loop since we are done with it
                prevhist[j][k] = hist[j][k]
                hist[j][k] = 0
        diff /= total
        return diff
