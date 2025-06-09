from typing import Iterable, Self
from dataclasses import dataclass
from functools import cached_property
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


@dataclass(frozen=True)
class PatternGenerator:
    target: Vec2
    max_pattern_len: int = 64

    @cached_property
    def patterns(self) -> list[Pattern]:
        raster = self.target.raster()
        return [
            Pattern(raster[:length], self.target)
            for length in range(2, min(len(raster), self.max_pattern_len + 1))
        ]

    @cached_property
    def pareto_front(self) -> list[Pattern]:
        return [
            pattern
            for pattern in self.patterns
            if not any([o_pattern.dominates(pattern) for o_pattern in self.patterns])
        ]

    @staticmethod
    def len_sorted(patterns: list[Pattern], short2long: bool = True) -> list[Pattern]:
        if short2long:
            return sorted(patterns, key=lambda p: len(p))
        return sorted(patterns, key=lambda p: -len(p))

    @staticmethod
    def deviation_sorted(patterns: list[Pattern], close2far: bool = True) -> list[Pattern]:
        if close2far:
            return sorted(patterns, key=lambda p: p.deviation())
        return sorted(patterns, key=lambda p: -p.deviation())

