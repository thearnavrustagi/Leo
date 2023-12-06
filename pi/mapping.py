from typing import Callable

import numpy as np
import matplotlib.pyplot as plt

from log_odds import log_odds, retrieve_p

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
        self.probability_map = np.ones(grid_size) * P_INIT
        self.map_ids = np.zeros(grid_size)

        for ix, iy in np.nindex(self.map_ids.shape):
            self.map_ids[ix, iy] = numbering_order(ix, iy)

        self.probability_history = [self.probability_map]

    def update_log_odds (self, 
            positions:List[Tuple[int]],
            probabilities:List[np.float64]) -> None:

        for (x, y), p in zip(positions, probabilities):
            self.log_odds_map[x,y] += log_odds(p)

        self.probability_map = retrieve_p(self.log_odds_map)
        self.probability_history.append(self.probability_map)

    def export(directory:str = "./mappings") -> None:
        for m_t in self.probability_history:
            maps = [m_t, discretize(m_t)]
            for i, m in enumerate(maps):
                plt.subplot(1, 2, i + 1)
                plt.imshow(m, cmap="binary")
                plt.colorbar()
            figure = plt.gcf()
            figure.set_sizes_inches(12,12)
            plt.savefig(f"{directory}/{i}.png")


def discretize_mapping(mymap=MAP, decision_boundary=DEC_BOUNDARY):
    return (mymap > decision_boundary).astype(np.float64)

if __name__ == "__main__":
    a = np.random.random((X, Y))
    a[1, 1] = 1
    a[1, 2] = 1
    a[1, 3] = 1
    a[1, 4] = 1
    a[1, 5] = 1
    show_map(a)
