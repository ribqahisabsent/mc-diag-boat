from math import sin, radians
from .reporting import SIG_FIGS


class Vec2:
    def __init__(self, x: float, z: float) -> None:
        self.x = x
        self.z = z

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.z + other.z)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.z - other.z)

    def __mul__(self, other: int | float) -> "Vec2":
        if isinstance(other, Vec2):
            return Vec2(0, 0)
        return Vec2(self.x * other, self.z * other)

    def __rmul__(self, other: int | float) -> "Vec2":
        return self.__mul__(other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.z})"

    def length(self) -> float:
        return (self.x**2 + self.z**2)**0.5

    def rounded(self, ndigits: int = 0) -> "Vec2":
        if ndigits == 0:
            return Vec2(round(self.x), round(self.z))
        return Vec2(round(self.x, ndigits), round(self.z, ndigits))


class TravelError:
    def __init__(self, angle_error: float, distance: float) -> None:
        self.angle = angle_error
        self.per_block = abs(2 * sin(radians(angle_error/2)))
        self.total = self.per_block * distance

    def __repr__(self) -> str:
        attrs = ", ".join(f"{key}={value:.{SIG_FIGS}}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"

