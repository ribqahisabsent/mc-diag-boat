from typing import Iterable
from dataclasses import dataclass
from functools import cached_property
from .vec2 import Vec2
from .optimization import pareto_indices


class Pattern(list[Vec2[int]]):
    def __init__(self, iterable: Iterable, target: Vec2) -> None:
        super().__init__(iterable)
        self.target = target

    def deviation(self) -> float:
        if len(self) <= 1:
            raise IndexError("Pattern with length <2 has no points to determine deviation")
        return (self.target - self.target.project(self[-1])).length()

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
        paretos = pareto_indices([
            (-pattern.deviation(), -len(pattern))
            for pattern in self.patterns
        ])
        return [self.patterns[index] for index in paretos]

    def len_sorted(self, short2long: bool = True) -> list[Pattern]:
        if short2long:
            return sorted(self.patterns, key=lambda p: len(p))
        return sorted(self.patterns, key=lambda p: -len(p))

    def deviation_sorted(self, close2far: bool = True) -> list[Pattern]:
        if close2far:
            return sorted(self.patterns, key=lambda p: p.deviation())
        return sorted(self.patterns, key=lambda p: -p.deviation())

