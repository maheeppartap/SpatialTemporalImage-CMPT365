from src.STImg import STImg

# OK so basically, when there is a cut, vert wipe, or hor wipe
# One of the the STI's will have an immediate change, and the other may or may not.
# so the plan is. We detect the sudden changes in both, (get the index), and then use
# the other one to characterize what type of transition it is
# and then maybe use that to draw over it when we display


class TransitionDetector:
    def __init__(self, colSTI: STImg, rowSTI: STImg):
        self.colSTI = colSTI
        self.rowSTI = rowSTI
        self.colhist = colSTI.histogram()
        self.rowhist = rowSTI.histogram()

    def do_da_ting(self):
        self._hor_trans_points()

    def _hor_trans_points(self):
        pass

    def _vert_trans_points(self):
        pass