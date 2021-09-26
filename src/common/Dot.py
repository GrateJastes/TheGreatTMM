class Dot:
    """Just a dot on the XoY plane, but with the generalized coordinate of the mechanism"""

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y


class AnalogDot(Dot):
    def __init__(self, dot, omega):
        super().__init__(dot.x, dot.y)
        self.omega = omega
