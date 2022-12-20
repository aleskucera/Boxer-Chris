import random
import numpy as np
import scipy.optimize as opt
from sklearn.cluster import DBSCAN


class Square:
    def __init__(self, x, y, width, height, rotation, contour, corners, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.contour = contour
        self.corners = corners
        self.color = color

    @property
    def area(self):
        return self.width * self.height

    @property
    def center(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return f"Square:\n  - (x,y):    ({self.x, self.y})" \
               f"       \n  - width:    {self.width}" \
               f"       \n  - height:   {self.height}" \
               f"       \n  - rotation: {self.rotation}" \
               f"       \n  - area:     {self.area}" \
               f"       \n  - color:    {self.color}"

    def __repr__(self):
        return f"{self.area}"


def cluster_squares(squares: np.ndarray, eps: float, min_samples: int) -> tuple:
    # get an array of the areas of the squares
    areas = np.array([[square.area] for square in squares])
    # cluster squares with similar areas
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(areas)
    return np.array(clustering.labels_, dtype=int)


def assemble_order(squares: np.ndarray, color_priority=False) -> np.ndarray:
    # divide squares into groups by their areas
    clusters = cluster_squares(squares, 0.4, 1)     # rearranged_squares
    idx_sort = np.argsort(clusters)
    squares = squares[idx_sort]
    clusters = clusters[idx_sort]

    squares = np.split(squares, np.where(np.diff(clusters) == 1)[0]+1)

    # TODO: DELETE THIS PART
    for i, gsquares in enumerate(squares):
        print(f"-------------------------------------\nGroup {i}:\n")
        for square in gsquares:
            print(square.area)
    # TODO: END

    colors = ["red", "black", "blue", "orange", "green"]

    # get a possible assemble order
    if color_priority:
        result = None
    else:
        l = get_longest_array(squares)
        A = np.full((len(squares), l), None)
        for i, square in enumerate(squares):
            A[i, :len(square)] = square
    print(A)
    return 0


def get_longest_array(arrays):
    lens = []
    for array in arrays:
        lens.append(len(array))
    return max(lens)

def main():
    squares = []
    colors = ["red", "black", "blue", "orange", "green"]
    for i in range(5):
        for color in colors:
            square = Square(random.uniform(-100,100), random.uniform(-100, 100), i+random.uniform(-0.1,0.1), i+random.uniform(-0.1, 0.1), 0, [], [], color)
            squares.append(square)
            # print(square)

    np.random.shuffle(squares)
    assemble_order(np.array(squares))


if __name__ == "__main__":
    main()
