from typing import Self
from math import sin, cos, radians
import skimage.draw
from .reporting import SIG_FIGS


class Vec2:
    def __init__(self, x: float | int, z: float | int) -> None:
        self.x = x
        self.z = z

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unsupported type(s) for +: '{type(self)}' and '{type(other)}'")
        return self.__class__(self.x + other.x, self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unsupported type(s) for -: '{type(self)}' and '{type(other)}'")
        return self.__class__(self.x - other.x, self.z - other.z)

    def __mul__(self, other: int | float) -> Self:
        if not isinstance(other, (int, float)):
            raise TypeError(f"Unsupported type(s) for *: '{type(self)}' and '{type(other)}'")
        return self.__class__(self.x * other, self.z * other)

    def __rmul__(self, other: int | float) -> Self:
        return self.__mul__(other)

    def __repr__(self) -> str:
        return f"({self.x}, {self.z})"

    @classmethod
    def from_polar(cls, rho: float, phi: float) -> Self:
        radian_phi = radians(phi)
        return cls((-1 * rho * sin(radian_phi)), (rho * cos(radian_phi)))

    def length(self) -> float:
        return (self.x**2 + self.z**2)**0.5

    def rounded(self, ndigits: int = 0) -> Self:
        if ndigits == 0:
            return self.__class__(round(self.x), round(self.z))
        return self.__class__(round(self.x, ndigits), round(self.z, ndigits))

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.z

    def raster(self, origin: Self | None = None) -> list[Self]:
        """Get the raster of the vector.
        """
        if origin is None:
            origin = self.__class__(0.0, 0.0)
        return [
            self.__class__(x, z)
            for x, z in zip(*skimage.draw.line_nd(origin, self.as_tuple(), endpoint=True))
        ]


class TravelError:
    def __init__(self, angle_error: float, distance: float) -> None:
        self.angle = angle_error
        self.per_block = abs(2 * sin(radians(angle_error/2)))
        self.total = self.per_block * distance

    def __repr__(self) -> str:
        attrs = ", ".join(f"{key}={value:.{SIG_FIGS}}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"

