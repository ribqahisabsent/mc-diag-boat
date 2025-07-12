from typing import ClassVar, Self, overload


class Angle(float):
    BOAT_ANGLE_STEP: ClassVar[Self]
    NORTH: ClassVar[Self]
    WEST: ClassVar[Self]
    SOUTH: ClassVar[Self]
    EAST: ClassVar[Self]
    ZERO: ClassVar[Self]
    BOAT_ANGLES: ClassVar[list[Self]]

    def __new__(cls, degrees: float) -> Self:
        return super().__new__(cls, (degrees + 180) % 360 - 180)

    def __pos__(self) -> Self:
        return type(self)(+self)

    def __neg__(self) -> Self:
        return type(self)(-self)

    def angular_dist(self, other: float) -> Self:
        return self.__class__((other - self + 180) % 360 - 180)

    @overload
    def closest_boat_angle(self) -> Self: ...
    @overload
    def closest_boat_angle(self, n: int) -> list[Self]: ...
    def closest_boat_angle(self, n: int | None = None) -> Self | list[Self]:
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

    def boat_placement_range(self) -> tuple[Self, Self] | None:
        boat_angle = self.closest_boat_angle()
        if boat_angle == 180.0 or boat_angle == -180.0:
            return None
        if boat_angle < 0.0:
            return self.__class__(boat_angle - self.BOAT_ANGLE_STEP), self
        if boat_angle > 0.0:
            return self, self.__class__(boat_angle + self.BOAT_ANGLE_STEP)
        return -self.BOAT_ANGLE_STEP, self.BOAT_ANGLE_STEP


Angle.BOAT_ANGLE_STEP = Angle(360 / 256)
Angle.NORTH = Angle(-180.0)
Angle.WEST = Angle(90.0)
Angle.SOUTH = Angle(0.0)
Angle.EAST = Angle(-90.0)
Angle.BOAT_ANGLES = [Angle(index * Angle.BOAT_ANGLE_STEP) for index in range(-128, 128)]

