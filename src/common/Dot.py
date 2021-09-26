class Dot:
    """Just a dot on the XoY plane, but with the generalized coordinate of the mechanism"""

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y


class AnalogDot(Dot):
    def __init__(self, coords, omega):
        super().__init__(coords[0], coords[1])
        self.omega = omega
