from src.STImg import STImg
import numpy as np


# OK so basically, when there is a cut, vert wipe, or hor wipe
# One of the the STI's will have an immediate change, and the other may or may not.
# so the plan is. We detect the sudden changes in both, (get the index), and then use
# the other one to characterize what type of transition it is
# and then maybe use that to draw over it when we display


class TransitionDetector:
    def __init__(self, colSTI: STImg, rowSTI: STImg):
        self.colSTI = colSTI
        self.rowSTI = rowSTI

    def do_da_ting(self):
        colt = self._detect_transitions(self.colSTI)
        rowt = self._detect_transitions(self.rowSTI)
        print(colt)
        print(rowt)

    @staticmethod
    def _detect_transitions(STI: STImg):
        frames = STI.frames
        rows = STI.rows
        n = STI.N
        hists = STI.histograms()
        trans = []
        for i in range(frames - 1):
            diff = 0
            for x in range(n):
                for y in range(n):
                    diff += min(hists[i][x][y], hists[i + 1][x][y])
            diff /= rows
            if diff < 0.5:
                trans.append(i)
        return trans
