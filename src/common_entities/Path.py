from __future__ import annotations

from .Dot import AnalogDot, Dot


class Path:
    """Represents the path of the point of interest"""
    dots: list[AnalogDot]
    missed_dots: int
    last_dot_coords: tuple

    def __init__(self):
        self.missed_dots = 0
        self.dots = []
        self.last_dot_coords = (None, None)

    def append(self, coords: tuple, scale: float = 1, time: float | None = None) -> None:
        if coords != (None, None):
            self.last_dot_coords = coords
            coords = self.rescale(coords, scale)

        self.dots.append(AnalogDot((coords[0], coords[1]), None, time))

    def rescale(self, coords, scale):
        return coords[0] * scale, coords[1] * scale
