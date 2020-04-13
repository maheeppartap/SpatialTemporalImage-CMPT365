import math


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
    def __lt__(self, other):
        return self.start < other.start

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

    # we need this because some transitions need fps to compute their start value
    def compute_statics(self):
        pass


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
    q = 1 - p
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
    duration = 0.7
    max_height = 0.3

    def __init__(self, start: int, r=255, g=192, b=203):
        self.at = 0
        self.bt = 0
        self.ct = 0
        self.major = 0
        self.major2 = 0
        self.minor = 0
        self.minor2 = 0
        self.hw = 0
        self.hh = 0
        self.max_distance = 0
        # make cut 1 second wide so we can enhance it more
        # todo: somehow make this dependant on fps
        super().__init__(start, start, r, g, b)

    def _distance_to_ellipse(self, rows, cols):
        # use an iterative method to solve for distance to ellipse
        px = abs(cols - self.hw)
        py = abs(rows - self.hh)
        tx = 0.707
        ty = 0.707
        for x in range(0, 3):
            x = self.major * tx
            y = self.minor * ty

            ex = (self.major2 - self.minor2) * tx ** 3 / self.major
            ey = (self.minor2 - self.major2) * ty ** 3 / self.minor

            rx = x - ex
            ry = y - ey

            qx = px - ex
            qy = py - ey

            r = math.hypot(ry, rx)
            q = math.hypot(qy, qx)

            tx = min(1, max(0, (qx * r / q + ex) / self.major))
            ty = min(1, max(0, (qy * r / q + ey) / self.minor))
            t = math.hypot(ty, tx)
            tx /= t
            ty /= t

        tx = math.copysign(self.major * tx, cols)
        ty = math.copysign(self.minor * ty, rows)
        return math.sqrt((tx-px)*(tx-px) + ((ty-py)*(ty-py)))

    def _set_ellipse_eqn(self, t):
        self.minor = self.at * (t * t) + self.bt * t + self.ct
        self.major = self.minor * Transition.vidspec.width / Transition.vidspec.height
        self.major2 = self.major * self.major
        self.minor2 = self.minor * self.minor
        self.max_distance = self._distance_to_ellipse(0, 0)

    def _blend_p(self, rows, cols):
        if (cols - self.hw)*(cols-self.hw) / self.major2 + (rows - self.hh)*(rows - self.hh) / self.minor2 < 1:
            return 0
        else:
            return self._distance_to_ellipse(rows, cols)/self.max_distance

    def draw_on_frame(self, frame, frame_ind) -> bool:
        super().draw_on_frame(frame, frame_ind)
        t = self._percent_complete(frame_ind)
        if t < 0:
            return False
        elif t > 1:
            return True

        self._set_ellipse_eqn(t)
        i = 0
        while i < Transition.vidspec.height:
            j = 0
            flipped = False
            while j < Transition.vidspec.width:
                p = self._blend_p(i, j)
                if p == 0:
                    # take advantage of the symmetric nature of our ellipse
                    if flipped:
                        i = Transition.vidspec.height-i
                        break
                    else:
                        j = Transition.vidspec.width-j+1
                        continue

                _blend(frame[i][j], p, self.r, self.g, self.b)
                j += 1
            i += 1

        return False

    def compute_statics(self):
        self.start -= int((self.duration / 2) * Transition.vidspec.fps)
        self.start = max(0, self.start)
        self.end += int(self.duration / 2 * Transition.vidspec.fps)
        self.end = min(Transition.vidspec.frames, self.end)
        self.at = Transition.vidspec.height * -2 * (1 - self.max_height - math.sqrt(2))
        self.bt = -1 * self.at
        self.ct = math.sqrt(2) / 2 * Transition.vidspec.height
        self.hw = Transition.vidspec.width / 2
        self.hh = Transition.vidspec.height / 2


# Null transition to mark end of transitions
class EmptyTrans(Transition):
    def __init__(self, start=999999999999, end=999999999999):
        super().__init__(start, end)

    def draw_on_frame(self, frame, frame_ind) -> bool:
        return False
