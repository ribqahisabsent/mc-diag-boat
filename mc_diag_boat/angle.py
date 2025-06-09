from typing import ClassVar, Self, overload
from math import radians, sin


class Angle(float):
    BOAT_ANGLE_STEP: ClassVar["Angle"]
    NORTH: ClassVar["Angle"]
    WEST: ClassVar["Angle"]
    SOUTH: ClassVar["Angle"]
    EAST: ClassVar["Angle"]
    ZERO: ClassVar["Angle"]
    BOAT_ANGLES: ClassVar[list["Angle"]]

    def __new__(cls, degrees: float) -> Self:
        return super().__new__(cls, (degrees + 180) % 360 - 180)

    def __pos__(self) -> Self:
        return type(self)(+self)

    def __neg__(self) -> Self:
        return type(self)(-self)

    def angular_dist(self, other: float) -> "Angle":
        return Angle((other - self + 180) % 360 - 180)

    def unit_deviation(self, other: float) -> float:
        return 2 * sin(radians(abs(self - other) / 2))

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
            return Angle(boat_angle - self.BOAT_ANGLE_STEP), self
        if boat_angle > 0.0:
            return self, Angle(boat_angle + self.BOAT_ANGLE_STEP)
        return -self.BOAT_ANGLE_STEP, self.BOAT_ANGLE_STEP


Angle.BOAT_ANGLE_STEP = Angle(360 / 256)
Angle.NORTH = Angle(-180.0)
Angle.WEST = Angle(90.0)
Angle.SOUTH = Angle(0.0)
Angle.EAST = Angle(-90.0)
Angle.BOAT_ANGLES = [Angle(index * Angle.BOAT_ANGLE_STEP) for index in range(-128, 128)]

