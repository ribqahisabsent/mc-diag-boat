from typing import Generic, Self, SupportsIndex, TypeVar, overload
from math import sin, cos, radians
import skimage.draw
from .reporting import SIG_FIGS


T = TypeVar("T", int, float)


class Vec2(Generic[T]):
    def __init__(self, x: T, z: T) -> None:
        self.x = x
        self.z = z

    @overload
    def __add__(self, other: "Vec2[int]") -> Self: ...
    @overload
    def __add__(self, other: "Vec2[float]") -> "Vec2[float]": ...
    def __add__(self, other: "Vec2[int] | Vec2[float]") -> Self | "Vec2[float]":
        if not isinstance(other, Vec2):
            raise TypeError(f"Unsupported type(s) for +: '{type(self)}' and '{type(other)}'")
        return Vec2(self.x + other.x, self.z + other.z)

    @overload
    def __sub__(self, other: "Vec2[int]") -> Self: ...
    @overload
    def __sub__(self, other: "Vec2[float]") -> "Vec2[float]": ...
    def __sub__(self, other: "Vec2[int] | Vec2[float]") -> Self | "Vec2[float]":
        if not isinstance(other, Vec2):
            raise TypeError(f"Unsupported type(s) for -: '{type(self)}' and '{type(other)}'")
        return Vec2(self.x - other.x, self.z - other.z)

    @overload
    def __mul__(self, scalar: SupportsIndex) -> Self: ...
    @overload
    def __mul__(self, scalar: float) -> "Vec2[float]": ...
    def __mul__(self, scalar: SupportsIndex | float) -> Self | "Vec2[float]":
        if isinstance(scalar, SupportsIndex):
            scalar = int(scalar)
            return type(self)(self.x * scalar, self.z * scalar)
        elif isinstance(scalar, float):
            return Vec2(self.x * scalar, self.z * scalar)
        raise TypeError(f"Unsupported type(s) for *: '{type(self)}' and '{type(scalar)}'")

    __rmul__ = __mul__

    def __truediv__(self, scalar: float) -> "Vec2[float]":
        return Vec2(self.x / scalar, self.z / scalar)

    @overload
    def __floordiv__(self, scalar: SupportsIndex) -> Self: ...
    @overload
    def __floordiv__(self, scalar: float) -> "Vec2[float]": ...
    def __floordiv__(self, scalar: SupportsIndex | float) -> Self | "Vec2[float]":
        if isinstance(scalar, SupportsIndex):
            scalar = int(scalar)
            return type(self)(self.x // scalar, self.z // scalar)
        elif isinstance(scalar, float):
            return Vec2(self.x // scalar, self.z // scalar)

    def __repr__(self) -> str:
        return f"({self.x}, {self.z})"

    @staticmethod
    def from_polar(rho: float, phi: float) -> "Vec2[float]":
        radian_phi = radians(phi)
        return Vec2((-1 * rho * sin(radian_phi)), (rho * cos(radian_phi)))

    def length(self) -> float:
        return (self.x**2 + self.z**2)**0.5

    @overload
    def rounded(self) -> "Vec2[int]": ...
    @overload
    def rounded(self, ndigits: SupportsIndex) -> "Vec2[float]": ...
    def rounded(self, ndigits: SupportsIndex | None = None) -> "Vec2[float] | Vec2[int]":
        if ndigits is None:
            return Vec2(round(self.x), round(self.z))
        return Vec2(round(self.x, ndigits), round(self.z, ndigits))

    def as_tuple(self) -> tuple[T, T]:
        return self.x, self.z

    def raster(self, origin: "Vec2 | None" = None) -> list["Vec2[int]"]:
        """Get the raster of the vector.
        """
        if origin is None:
            origin = Vec2(0, 0)
        return [
            Vec2(int(x), int(z))
            for x, z in zip(*skimage.draw.line_nd(origin.as_tuple(), self.as_tuple(), endpoint=True))
        ]


class TravelError:
    def __init__(self, angle_error: float, distance: float) -> None:
        self.angle = angle_error
        self.per_block = abs(2 * sin(radians(angle_error/2)))
        self.total = self.per_block * distance

    def __repr__(self) -> str:
        attrs = ", ".join(f"{key}={value:.{SIG_FIGS}}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"

