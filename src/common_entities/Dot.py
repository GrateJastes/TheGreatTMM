import math


class Dot:
    """Just a dot on the XoY plane, but with the generalized coordinate of the mechanism"""
    x: int
    y: int

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def traverse_coords(self, origin: tuple) -> None:
        if self.x is None:
            return

        self.x = self.x - origin[0]
        self.y = - self.y + origin[1]


class AnalogDot(Dot):
    omega: float
    time: float

    def __init__(self, coords, omega, time):
        super().__init__(coords[0], coords[1])
        self.omega = omega
        self.time = time

    def set_self_omega(self):
        if self.x is None:
            return

        self.omega = math.atan2(self.y, self.x)
