import numpy as np
import matplotlib.pyplot as plt

X,Y = 10,10
MAP = [[0]*Y for _ in range(X)]

def map_from_probability (
        positions : list,
        probabilities : list) -> None:

    for (x,y), p in zip(positions, probabilities):
        MAP[x][y] = p

def discretize(
        mymap=MAP,
        decision_boundary=0.5):
    return (mymap > decision_boundary).astype(np.float64)

def show_map (mymap=MAP) -> None:
    maps = [
            mymap, 
            discretize(mymap)
            ]
    for i,m in enumerate(maps):
        plt.subplot(1,2,i+1)
        plt.imshow(m, cmap="binary")
        plt.colorbar()
    plt.show()

if __name__ == "__main__":
    a = np.random.random((X, Y))
    a[1,1] = 1
    a[1,2] = 1
    a[1,3] = 1
    a[1,4] = 1
    a[1,5] = 1
    show_map (a)

