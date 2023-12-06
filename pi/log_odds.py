import numpy as np
from numpy.typing import NDArray

# p is the probability of the grid being occupied or not. this we need to define based on repeated measurements.

def log_odds(p: NDArray[NDArray[np.float64]]) -> NDArray[NDArray[np.float64]]:
    """
    Log odds ratio of p(x):

                   p(x)
     l(x) = log ----------
                 1 - p(x)

    """
    if p == 0:
        # a lesser float to prevent overflow
        return np.finfo(np.float32).min
    return np.log(p / (1 - p))


def retrieve_p(l: NDArray[NDArray[np.float64]]) -> NDArray[NDArray[np.float64]]:
    """
    Retrieve p(x) from log odds ratio:

                       1
     p(x) = 1 - ---------------
                 1 + exp(l(x))

    """
    return 1 - 1 / (1 + np.exp(l))
