from typing import Sequence
import numpy as np


def pareto_indices(points: Sequence[Sequence] | np.ndarray) -> np.ndarray:
    points = np.array(points)
    return np.where(np.apply_along_axis(
            lambda p: ~np.any(np.all(points >= p, axis=1) & np.any(points > p, axis=1)),
            axis=1,
            arr=points,
    ))[0]

