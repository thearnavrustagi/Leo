from typing import Callable

import numpy as np
import matplotlib.pyplot as plt

X, Y = 10, 10
MAP = [[0] * Y for _ in range(X)]


class Mapping(object):
    def __init__(self,
            grid_size:tuple,
            numbering_order:Callable,
            increment:int):
        self.grid_size = grid_size
        self.numbering_order = numbering_order
        self.increment = increment

        self.log_odds_map = np.zeros(grid_size)
        self.probability_map = np.zeros(grid_size)
        self.map_ids = np.zeros(grid_size)

        for ix, iy in np.nindex(self.map_ids.shape):
            self.map_ids[ix, iy] = numbering_order(ix, iy)

        self.probability_history = []

    def map_from_probability(
            positions: List[List[np.float64]],
            probabilities: List[np.float64]) -> None:
        for (x, y), p in zip(positions, probabilities):
            MAP[x][y] = p


    def discretize_mapping(mymap=MAP, decision_boundary=0.5):
        return (mymap > decision_boundary).astype(np.float64)

    def save_mapping(mymap=MAP) -> None:
        maps = [mymap, discretize(mymap)]
        for i, m in enumerate(maps):
            plt.subplot(1, 2, i + 1)
            plt.imshow(m, cmap="binary")
            plt.colorbar()
        figure = plt.gcf()
        figure.set_sizes_inches(16,16)
        plt.savefig("./map.png")


if __name__ == "__main__":
    a = np.random.random((X, Y))
    a[1, 1] = 1
    a[1, 2] = 1
    a[1, 3] = 1
    a[1, 4] = 1
    a[1, 5] = 1
    show_map(a)
