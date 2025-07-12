from types import ModuleType
from typing import Iterable
from dataclasses import dataclass
from functools import cached_property
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from .vec2 import Vec2
from .optimization import pareto_indices


class Pattern(list[Vec2[int]]):
    MIN_PLOT_COLOR = 0.12

    def __init__(self, iterable: Iterable, target: Vec2) -> None:
        super().__init__(iterable)
        self.target = target

    def deviation(self) -> float:
        if len(self) <= 1:
            raise IndexError("Pattern with length <2 has no points to determine deviation")
        return (self.target - self.target.project(self[-1])).length()

    # Display a 2D map representing the blocks in a given pattern
    def plot(self) -> tuple[Figure, ModuleType]:
        pattern_space = np.zeros((abs(self[-1].x) + 1, abs(self[-1].z) + 1))
        for index, point in enumerate(self[:-1]):
            pattern_space[(abs(point.x), abs(point.z))] = (len(self) - index) / len(self) + self.MIN_PLOT_COLOR
        pattern_space[(abs(self[-1].x), abs(self[-1].z))] = 1.0 + self.MIN_PLOT_COLOR
        pattern_space = np.transpose(pattern_space)
        fig, ax = plt.subplots()
        ax.imshow(pattern_space, cmap="turbo", interpolation="nearest")
        if self[-1].x < 0:
            fig.gca().invert_xaxis()
        if self[-1].z < 0:
            fig.gca().invert_yaxis()
        ax.set_title("Start at red (0, 0), follow rainbow\n(lone red is start of next iteration)")
        ax.set_xlabel("West < - > East")
        ax.set_ylabel("South < - > North")
        ax.set_xticks(
            [i for i in range(abs(self[-1].x) + 1)],
            [str(i) for i in range(abs(self[-1].x) + 1)],
            rotation=90
        )
        ax.set_yticks([i for i in range(abs(self[-1].z) + 1)])
        return fig, plt

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

