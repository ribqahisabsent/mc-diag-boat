from typing import ClassVar, Generic, Self, SupportsIndex, TypeVar, overload
from math import radians, degrees, sin, cos, atan2
import skimage.draw
from .reporting import SIG_FIGS


_T = TypeVar("_T", int, float)


class Vec2(Generic[_T]):
    x: _T
    z: _T

    NORTH: ClassVar["Vec2[int]"]
    WEST: ClassVar["Vec2[int]"]
    SOUTH: ClassVar["Vec2[int]"]
    EAST: ClassVar["Vec2[int]"]
    ZERO: ClassVar["Vec2[int]"]
    ZERODEG: ClassVar["Vec2[int]"]

    def __init__(self, x: _T, z: _T) -> None:
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

    def length(self) -> float:
        return (self.x**2 + self.z**2)**0.5

    def angle(self) -> float:
        return -1 * degrees(atan2(self.x, self.z))

    def rotated(self, angle: float) -> "Vec2[float]":
        radian_angle = radians(angle)
        angle_cos = cos(radian_angle)
        angle_sin = sin(radian_angle)
        return Vec2(
            self.x * angle_cos - self.z * angle_sin,
            self.x * angle_sin + self.z * angle_cos,
        )

    @overload
    def rounded(self) -> "Vec2[int]": ...
    @overload
    def rounded(self, ndigits: SupportsIndex) -> "Vec2[float]": ...
    def rounded(self, ndigits: SupportsIndex | None = None) -> "Vec2[float] | Vec2[int]":
        if ndigits is None:
            return Vec2(round(self.x), round(self.z))
        return Vec2(round(self.x, ndigits), round(self.z, ndigits))

    def as_tuple(self) -> tuple[_T, _T]:
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


Vec2.NORTH = Vec2(0, -1)
Vec2.WEST = Vec2(-1, 0)
Vec2.SOUTH = Vec2(0, 1)
Vec2.EAST = Vec2(1, 0)
Vec2.ZERO = Vec2(0, 0)
Vec2.ZERODEG = Vec2.SOUTH


class TravelError:
    def __init__(self, angle_error: float, distance: float) -> None:
        self.angle = angle_error
        self.per_block = abs(2 * sin(radians(angle_error/2)))
        self.total = self.per_block * distance

    def __repr__(self) -> str:
        attrs = ", ".join(f"{key}={value:.{SIG_FIGS}}" for key, value in vars(self).items())
        return f"{type(self).__name__}({attrs})"

