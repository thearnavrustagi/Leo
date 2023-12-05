import numpy as np
import numpy.typing as npt
from typing import List, Tuple

from priority_queue import PriorityQueue
from errors import NoPathError, IllegalStartPositionError
from constants import OCCUPIED, FREE


class AStar(object):
    def __init__(
        self,
        grid: List[List[np.float64]],
        start: Tuple[np.float64],
        goal: Tuple[np.float64],
    ):
        super().__init__()

        self.grid = grid
        self.start = start
        self.goal = goal

        self.path = [self.start]
        self.queue = PriorityQueue()

    def find_path(self):
        if self.grid[self.start] == OCCUPIED:
            raise IllegalStartPositionError(self.start)
