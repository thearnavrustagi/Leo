import numpy as np
from numpy.typing import NDArray

# p is the probability of the grid being occupied or not. this we need to define based on repeated measurements.


def compute_map_probability(probs: NDArray[np.float64]) -> NDArray[np.float64]:
    return [__retrieve_p__(__log_odds__(p)) for p in probs]


def __log_odds__(p: np.float64) -> np.float64:
    """
    Log odds ratio of p(x):

                   p(x)
     l(x) = log ----------
                 1 - p(x)

    """
    if p == 0:
        raise 
    return np.log(p / (1 - p))


def __retrieve_p__(l: np.float64) -> np.float64:
    """
    Retrieve p(x) from log odds ratio:

                       1
     p(x) = 1 - ---------------
                 1 + exp(l(x))

    """
    return 1 - 1 / (1 + np.exp(l))
