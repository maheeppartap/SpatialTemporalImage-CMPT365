from src.STImg import STImg

# OK so basically, when there is a cut, vert wipe, or hor wipe
# One of the the STI's will have an immediate change, and the other may or may not.
# so the plan is. We detect the sudden changes in both, (get the index), and then use
# the other one to characterize what type of transition it is
# and then maybe use that to draw over it when we display


class TransitionDetector:
    def __init__(self, vertSTI: STImg, horSTI: STImg):
        self.vertSTI = vertSTI
        self.horSTI = horSTI

    def hor_trans_points(self):
        pass

    def vert_trans_points(self):
        pass