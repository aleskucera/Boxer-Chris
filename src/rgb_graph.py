import numpy as np
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TkAgg')


def plot_rgb_graph(image: np.ndarray, k: int = 5) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(image[::k, ::k, 0].flatten(), image[::k, ::k, 1].flatten(),
               image[::k, ::k, 2].flatten(), c=image[::k, ::k, :].flatten().reshape(-1, 3), marker='o', s=5)

    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')

    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_zlim([0, 1])

    plt.show()


if __name__ == '__main__':
    img = plt.imread('../colors/red.png')
    plot_rgb_graph(img)

