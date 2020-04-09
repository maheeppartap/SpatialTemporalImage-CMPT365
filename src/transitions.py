class Transition:
    vidspec = None

    def __init__(self, start: int, end: int, r=255, g=128, b=70):
        # which frame the transition starts and ends on
        self.start = start
        self.end = end
        self.r = r
        self.g = g
        self.b = b

    # for sorting
    def __cmp__(self, other):
        if other is Transition:
            return self.start - other.start
        else:
            return 0

    def set_rgb(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    # draws something onto the frame to make the transition more prominent
    # returns True if the transition ends before frame_ind
    def draw_on_frame(self, frame, frame_ind) -> bool:
        if Transition.vidspec is None:
            print("IMPORTANT! set vidstats before enhancing video")
        return False

    # if start < frame < end, 0 < percent < 1
    def _percent_complete(self, frame):
        return (frame - self.start) / (self.end - self.start)


# utility methods
def _width_cap(col) -> int:
    return int(min(Transition.vidspec.width, col))


def _height_cap(row) -> int:
    return int(min(Transition.vidspec.height, row))


def _scale_up_width(val) -> float:
    return Transition.vidspec.width * val


def _scale_up_height(val) -> float:
    return Transition.vidspec.height * val


# quadratic probability value, for some offset i
# s represents the peak
# a is -1/r^2 where r is a width
def _blend_p(i, s, a) -> float:
    return max(0, a * (s - i) * (s - i) + 1)


def _blend(frame, p, r, g, b):
    q = 1-p
    frame[0] = q * frame[0] + p * r
    frame[1] = q * frame[1] + p * g
    frame[2] = q * frame[2] + p * b


class ColWipe(Transition):
    ridge_width = 0.1

    def __init__(self, start: int, end: int, scol: int, ecol: int, r=255, g=192, b=203):
        super().__init__(start, end, r, g, b)
        self.scol = scol
        self.ecol = ecol

    # find the spine of the ridge
    def _spine(self, t) -> float:
        return _scale_up_width(((self.ecol - self.scol) * t) + self.scol)

    # radius of ridge (width/2)
    def _radius(self) -> float:
        return _scale_up_width(self.ridge_width / 2)

    def draw_on_frame(self, frame, frame_ind) -> bool:
        super().draw_on_frame(frame, frame_ind)
        t = self._percent_complete(frame_ind)
        if t < 0:
            return False
        elif t > 1:
            return True

        # get variables for the equation a(i-s)^2 + 1
        # this is our blend parabola
        s = self._spine(t)
        r = self._radius()
        # set a so that (s-r) and (s+r) are roots to the parabola
        a = -1 / (r * r)
        # from the left of the spine to the right of the spine
        for i in range(int(max(s - r - 1, 0)), _width_cap(s + r + 1)):
            p = _blend_p(i, s, a)
            for j in range(Transition.vidspec.height):
                _blend(frame[j][i], p, self.r, self.g, self.b)
        return False


class HorWipe(Transition):
    ridge_width = 0.1

    def __init__(self, start: int, end: int, srow: int, erow: int, r=255, g=128, b=70):
        super().__init__(start, end, r, g, b)
        self.srow = srow
        self.erow = erow

    # find the spine of the ridge
    def _spine(self, t) -> float:
        return _scale_up_height(((self.erow - self.srow) * t) + self.srow)

    # radius of ridge (width/2)
    def _radius(self) -> float:
        return _scale_up_height(self.ridge_width / 2)

    def draw_on_frame(self, frame, frame_ind) -> bool:
        super().draw_on_frame(frame, frame_ind)
        t = self._percent_complete(frame_ind)
        if t < 0:
            return False
        elif t > 1:
            return True

        # get variables for the equation a(i-s)^2 + 1
        # this is our blend parabola
        s = self._spine(t)
        r = self._radius()
        # set a so that (s-r) and (s+r) are roots to the parabola
        a = -1 / (r * r)
        # from the left of the spine to the right of the spine
        for i in range(int(max(s - r - 1, 0)), _height_cap(s + r + 1)):
            p = _blend_p(i, s, a)
            for j in range(Transition.vidspec.width):
                _blend(frame[i][j], p, self.r, self.g, self.b)
        return False


class Cut(Transition):
    def __init__(self, start: int, r=255, g=128, b=70):
        # make cut 1 second wide so we can enhance it more
        super().__init__(start, start, r, g, b)

    def draw_on_frame(self, frame, frame_ind) -> bool:
        super().draw_on_frame(frame, frame_ind)
        t = self._percent_complete(frame_ind)
        if t < 0:
            return False
        elif t > 1:
            return True

        return False


# Null transition to mark end of transitions
class EmptyTrans(Transition):
    def __init__(self, start=0, end=0):
        super().__init__(start, end)

    def draw_on_frame(self, frame, frame_ind) -> bool:
        return False
