from typing import Callable, ClassVar, Self, overload
from math import radians, sin


BOAT_ANGLE_STEP = 360 / 256


class Angle(float):
    NORTH: ClassVar["Angle"]
    WEST: ClassVar["Angle"]
    SOUTH: ClassVar["Angle"]
    EAST: ClassVar["Angle"]
    ZERO: ClassVar["Angle"]

    def unit_deviation(self, other: Self) -> float:
        return 2 * sin(radians(abs(self - other) / 2))


Angle.NORTH = Angle(-180.0)
Angle.WEST = Angle(90.0)
Angle.SOUTH = Angle(0.0)
Angle.EAST = Angle(-90.0)


class BoatAngle(Angle):
    def __new__(cls, index: int) -> Self:
        obj = super().__new__(cls, ((index + 128) % 256 - 128) * BOAT_ANGLE_STEP)
        return obj

    @staticmethod
    def closest_index(angle: float) -> int:
        mc_angle = (angle + 180) % 360 - 180
        return round(mc_angle / BOAT_ANGLE_STEP) % 256

    @classmethod
    @overload
    def closest_to(cls, angle: float) -> Self: ...
    @classmethod
    @overload
    def closest_to(cls, angle: float, n: int) -> list[Self]: ...
    @classmethod
    def closest_to(cls, angle: float, n: int | None = None) -> Self | list[Self]:
        mc_angle = (angle + 180) % 360 - 180
        if n is None:
            closest_index = cls.closest_index(mc_angle)
            closest_to = cls(closest_index)
            return closest_to
        sorted_indices = sorted([
            (index, ((cls(index) - mc_angle + 180) % 360) - 180)
            for index in range(256)
        ], key=lambda x: abs(x[1]))
        return [cls(index) for index, _ in sorted_indices[:n]]

    def index(self) -> int:
        mc_angle = (self + 180) % 360 - 180
        return round(mc_angle / BOAT_ANGLE_STEP) % 256

    def placement_range(self) -> tuple[Self, Self] | None:
        if self == 180.0 or self == -180.0:
            return None
        if self < 0.0:
            return type(self)(self.index() - 1), self
        if self > 0.0:
            return self, type(self)(self.index() + 1)
        return type(self)(-1), type(self)(1)


def block_arith() -> Callable:
    def blocked(self, *args, **kwargs):
        raise TypeError("BoatAngle should not be modified arithmetically.")
    return blocked


for method in [
    "__add__",
    "__radd__",
    "__sub__",
    "__rsub__",
    "__mul__",
    "__rmul__",
    "__truediv__",
    "__rtruediv__",
    "__floordiv__",
    "__rfloordiv__",
    "__mod__",
    "__rmod__",
    "__pow__",
    "__rpow__",
    "__neg__",
    "__pos__",
    "__abs__",
]:
    setattr(BoatAngle, method, block_arith())

