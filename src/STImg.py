import numpy as np
import traceback


class STImg:
    def __init__(self, rows, cols):
        # made this make more sense
        self.sti = np.zeros((int(rows), int(cols), 3))

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
