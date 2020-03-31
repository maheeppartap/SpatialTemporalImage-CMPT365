import numpy as np
import traceback


class STImg:
    # rows of an sti represents the # of rows or cols in the videos dimentions
    # cols represents the # frames in the video
    def __init__(self, rows, cols):

        # made this make more sense
        self.rows = int(rows)
        self.cols = int(cols)
        self.sti = np.zeros((self.rows, self.cols, 3))
        self.N = 1 + int(np.floor(np.log2(self.rows)))
        self.hists = np.zeros((self.cols, self.N, self.N))
        self.generated = False

    # adds a column at pos index for col STI. Default way.
    def addCol(self, pos, col):
        try:
            self.sti[:, pos] = col
        except ValueError:
            print("Invalid column input.")
            traceback.print_exc()

    # todo: use this to add individual elements to make a diagonal STI
    def addSingleElements(self, position, num):
        pass  # only for compiling purpose

    # adds a row for row STI. Could use, but meh.
    def addRow(self, pos, row):
        try:
            self.sti[:, pos] = row
        except ValueError:
            print("Invalid row input.")
            traceback.print_exc()

    def print(self):
        print(self.sti)

    def _generate_hists(self):
        self.generated = True
        for i in range(self.rows):
            for j in range(self.cols):
                sum = self.sti[i][j][0] + self.sti[i][j][1] + self.sti[i][j][2]
                if sum == 0:
                    r = 0
                    g = 0
                else:
                    r = self.sti[i][j][0] / sum
                    g = self.sti[i][j][1] / sum
                # quantize chromaticity
                rN = int(np.floor(r * (self.N-1)))
                gN = int(np.floor(g * (self.N-1)))
                self.hists[j][rN][gN] += 1

    def histogram(self):
        if not self.generated:
            self._generate_hists()
        return self.hists
