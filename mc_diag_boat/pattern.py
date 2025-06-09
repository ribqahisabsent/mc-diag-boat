from typing import Iterable, Self
from dataclasses import dataclass
from .vec2 import Vec2


class Pattern(list[Vec2[int]]):
    def __init__(self, iterable: Iterable, target: Vec2) -> None:
        super().__init__(iterable)
        self.target = target

    def deviation(self) -> float:
        if len(self) <= 1:
            raise IndexError("Pattern with length 1 has no points to determine deviation")
        return (self.target - self.target.project(self[-1])).length()

    def dominates(self, other: Self) -> bool:
        if self is other:
            return False
        s_dev = self.deviation()
        o_dev = other.deviation()
        if len(self) <= len(other) and s_dev <= o_dev:
            return len(self) < len(other) or s_dev < o_dev
        return False


@dataclass(slots=True)
class PatternGenerator:
    target: Vec2
    max_pattern_len: int
    patterns: list[Pattern]

    def __init__(self, target: Vec2, max_pattern_len: int = 64) -> None:
        self.target = target
        self.max_pattern_len = max_pattern_len
        self.patterns = []

    def generate(self) -> None:
        raster = self.target.raster()
        self.patterns = [
            Pattern(raster[:length], self.target)
            for length in range(2, min(len(raster), self.max_pattern_len + 1))
        ]

    def pareto_front(self) -> list[Pattern]:
        return [
            pattern
            for pattern in self.patterns
            if not any([o_pattern.dominates(pattern) for o_pattern in self.patterns])
        ]

