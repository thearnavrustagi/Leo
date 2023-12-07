from typing import Callable, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from log_odds import log_odds, retrieve_p
from constants import MAP_SIZE, L2R, T2B, DEC_BOUNDARY, P_INIT, FIG_SIZE

class Mapping(object):
    def __init__(self,
            grid_size:tuple,
            numbering_order:Tuple[Callable],
            increment:int):
        self.grid_size = grid_size
        (self.posn_to_idx, self.idx_to_posn) = numbering_order
        self.increment = increment

        self.log_odds_map = np.zeros(grid_size)
        self.probability_map = np.ones(grid_size) * P_INIT
        self.map_ids = np.zeros(grid_size)

        for ix, iy in np.ndindex(self.map_ids.shape):
            self.map_ids[ix, iy] = self.posn_to_idx(ix, iy, self.grid_size)

        self.probability_history = [self.probability_map]

    def update_log_odds (self, 
            positions:List[Tuple[int]],
            probabilities:List[np.float64]) -> None:

        print("probs",probabilities,"\nposns", positions)
        for (x, y), p in zip(positions, probabilities):
            if x not in range(0,MAP_SIZE[0]): continue
            if y not in range(0,MAP_SIZE[1]): continue

            self.log_odds_map[x,y] += log_odds(p)
            print(self.log_odds_map[x,y])

        self.probability_map = retrieve_p(self.log_odds_map)
        self.probability_history.append(self.probability_map)

    def export(self,directory:str = "./mappings") -> None:
        for im,m_t in enumerate(self.probability_history):
            maps = [(m_t,"probability map"), (discretize_mapping(m_t),"probability with decision boundary")]
            plt.clf()
            for i, (m,t) in enumerate(maps):
                plt.subplot(1, 2, i + 1)
                plt.title(t)
                plt.pcolor(np.column_stack(m), cmap="magma_r", vmin=0, vmax=1)
                plt.colorbar()
                plt.xticks(range(self.grid_size[0]))
                plt.yticks(range(self.grid_size[1]))
                plt.gca().set_aspect('equal')
                plt.grid(True, color="black")
                for i in range(self.grid_size[0]):
                    for j in range(self.grid_size[1]):
                        text = plt.text(i+0.5, j+0.5, str(self.posn_to_idx(i, j,self.grid_size)),
                                       ha="center", va="center", color="w")
            figure = plt.gcf()
            figure.set_size_inches(*FIG_SIZE)
            plt.savefig(f"{directory}/{im}.png")
        plt.savefig(f"final_map.png")


def discretize_mapping(mapping, decision_boundary=DEC_BOUNDARY):
    return (mapping > decision_boundary).astype(np.float64)

if __name__ == "__main__":
    print(MAP_SIZE)
    mapping = Mapping(MAP_SIZE, L2R, 1)
    mapping.update_log_odds([(1,0),(1,1),(1,2),(1,3),(1,4)],[0.4,0.4,0.4,0.6])
    mapping.update_log_odds([(1,1),(2,1),(3,1),(4,1)],[0.4,0.4,0.4,0.6])

    mapping.export()
