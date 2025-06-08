from typing import ClassVar, Self, overload
from dataclasses import dataclass
from math import radians, sin


@dataclass(frozen=True, slots=True)
class Angle:
    degrees: float

    BOAT_ANGLE_STEP: ClassVar["Angle"]
    NORTH: ClassVar["Angle"]
    WEST: ClassVar["Angle"]
    SOUTH: ClassVar["Angle"]
    EAST: ClassVar["Angle"]
    ZERO: ClassVar["Angle"]
    BOAT_ANGLES: ClassVar[list["Angle"]]

    def __post_init__(self):
        normalized = (self.degrees + 180) % 360 - 180
        object.__setattr__(self, "degrees", normalized)

    def __add__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((self.degrees + other + 180) % 360 - 180)

    __radd__ = __add__

    def __sub__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((self.degrees - other + 180) % 360 - 180)

    def __rsub__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((other - self.degrees + 180) % 360 - 180)

    def __mul__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((self.degrees * other + 180) % 360 - 180)

    __rmul__ = __mul__

    def __truediv__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((self.degrees / other + 180) % 360 - 180)

    def __rtruediv__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((other / self.degrees + 180) % 360 - 180)

    def __floordiv__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((self.degrees // other + 180) % 360 - 180)

    def __rfloordiv__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((other // self.degrees + 180) % 360 - 180)

    def __mod__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((self.degrees % other + 180) % 360 - 180)

    def __rmod__(self, other: "float | Angle") -> Self:
        if isinstance(other, Angle):
            other = other.degrees
        return type(self)((other % self.degrees + 180) % 360 - 180)

    def __pos__(self) -> Self:
        return type(self)(+self.degrees)

    def __neg__(self) -> Self:
        return type(self)(-self.degrees)

    def __abs__(self) -> Self:
        return type(self)(abs(self.degrees))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Angle):
            other = other.degrees
        return self.degrees == other

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Angle):
            other = other.degrees
        return self.degrees != other

    def __lt__(self, other: "float | Angle") -> bool:
        if isinstance(other, Angle):
            other = other.degrees
        return self.degrees < other

    def __le__(self, other: "float | Angle") -> bool:
        if isinstance(other, Angle):
            other = other.degrees
        return self.degrees <= other

    def __gt__(self, other: "float | Angle") -> bool:
        if isinstance(other, Angle):
            other = other.degrees
        return self.degrees > other

    def __ge__(self, other: "float | Angle") -> bool:
        if isinstance(other, Angle):
            other = other.degrees
        return self.degrees >= other

    def __int__(self) -> int:
        return int(self.degrees)

    def __float__(self) -> float:
        return float(self.degrees)

    def __bool__(self) -> bool:
        return bool(self.degrees)

    def __str__(self) -> str:
        return str(self.degrees)

    def __repr__(self) -> str:
        return self.degrees.__repr__()

    def __round__(self, n: int) -> Self:
        return type(self)(round(self.degrees, n))

    def angular_dist(self, other: "float | Angle") -> "Angle":
        if isinstance(other, Angle):
            other = other.degrees
        return Angle((other - self.degrees + 180) % 360 - 180)

    def unit_deviation(self, other: "float | Angle") -> float:
        if isinstance(other, Angle):
            other = other.degrees
        return 2 * sin(radians(abs(self.degrees - other) / 2))

    @overload
    def closest_boat_angle(self) -> "Angle": ...
    @overload
    def closest_boat_angle(self, n: int) -> list["Angle"]: ...
    def closest_boat_angle(self, n: int | None = None) -> "Angle | list[Angle]":
        sorted_boat_angles = sorted(
            self.BOAT_ANGLES,
            key=lambda x: abs(self.angular_dist(x))
        )
        if n is None or n == 1:
            return sorted_boat_angles[0]
        if n == -1:
            n = 256
        if 0 < n <= 256:
            return sorted_boat_angles[:n]
        raise ValueError("n must be -1 or in [1, 256]")

    def boat_placement_range(self) -> tuple["Angle", "Angle"] | None:
        boat_angle = self.closest_boat_angle()
        if boat_angle == 180.0 or boat_angle == -180.0:
            return None
        if boat_angle < 0.0:
            return boat_angle - self.BOAT_ANGLE_STEP, self
        if boat_angle > 0.0:
            return self, boat_angle + self.BOAT_ANGLE_STEP
        return -self.BOAT_ANGLE_STEP, self.BOAT_ANGLE_STEP


Angle.BOAT_ANGLE_STEP = Angle(360 / 256)
Angle.NORTH = Angle(-180.0)
Angle.WEST = Angle(90.0)
Angle.SOUTH = Angle(0.0)
Angle.EAST = Angle(-90.0)
Angle.BOAT_ANGLES = [index * Angle.BOAT_ANGLE_STEP for index in range(-128, 128)]

