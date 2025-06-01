from typing import Self, overload


ANGLE_STEP = 360 / 256


class BoatAngle(float):
    @staticmethod
    def closest_index(angle: float) -> int:
        mc_angle = (angle + 180) % 360 - 180
        return round(mc_angle / ANGLE_STEP) % 256

    @classmethod
    def from_index(cls, index: int) -> Self:
        return cls(((index + 128) % 256 - 128) * ANGLE_STEP)

    @classmethod
    @overload
    def closest_to(cls, angle: float) -> Self: ...
    @classmethod
    @overload
    def closest_to(cls, angle: float, n: int) -> list[Self]: ...
    @classmethod
    def closest_to(cls, angle: float, n: int | None = None) -> Self | list[Self]:
        mc_angle = (angle + 180) % 360 - 180
        closest_index = cls.closest_index(mc_angle)
        closest_to = cls.from_index(closest_index)
        if n is None:
            return closest_to
        sorted_indices = sorted([
            (index, ((cls.from_index(index) - mc_angle + 180) % 360) - 180)
            for index in range(256)
        ], key=lambda x: abs(x[1]))
        return [cls.from_index(index) for index, _ in sorted_indices[:n]]

    def index(self) -> int:
        mc_angle = (self + 180) % 360 - 180
        return round(mc_angle / ANGLE_STEP) % 256

