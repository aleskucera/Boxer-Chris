import numpy as np
import random
import scipy.optimize as opt


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


def assemble_order(squares: np.ndarray, color_priority=False) -> np.ndarray:
    # get an array of area of the squares
    areas = np.array([square.area for square in squares])

    # divide squares into groups by their areas
    r_squares = np.split(squares, np.flatnonzero(np.abs(np.diff(areas)) >= 0.5)+1)     # rearranged_squares
    print("here:", np.flatnonzero(np.abs(np.diff(areas)) >= 0.5)+1)
    # TODO: DELETE THIS PART
    for i, gsquares in enumerate(r_squares):
        print(f"-------------------------------------\nGroup {i}:\n")
        for square in gsquares:
            print(square.area)
    # TODO: END

    colors = ["red", "black", "blue", "orange", "green"]

    NUMBER_OF_COLORS = 6
    # get a possible assemble order
    result = [[]]*NUMBER_OF_COLORS
    if color_priority:
        result = np.split(squares, [1])
    else:
        return 1
    return result


def optimized_func(x, cam, glob):
    a11, a21, a12, a22, b1, b2 = x
    x_cam = cam[0, :]
    y_cam = cam[1, :]

    x_glob = glob[0, :]
    y_glob = glob[1, :]

    ones = np.ones_like(x_cam)

    f1 = a11*x_cam+a12*y_cam+ones*b1-x_glob
    f2 = a21*x_cam+a22*y_cam+ones*b2-y_glob

    return np.hstack((f1, f2))


def get_transform_parameters(X, Y):
    x0 = [1, 0, 0, 1, 0, 0]
    x = opt.least_squares(optimized_func, x0, args=(X, Y)).x
    a11, a21, a12, a22, b1, b2 = x

    return np.array([[a11, a12], [a21, a22]]), np.array([b1, b2])


def main():
    # squares = []
    # colors = ["red", "black", "blue", "orange", "green"]
    # for i in range(5):
    #     for color in colors:
    #         square = Square(random.uniform(-100,100), random.uniform(-100, 100), i+random.uniform(-0.1,0.1), i+random.uniform(-0.1, 0.1), 0, [], [], color)
    #         squares.append(square)
    #         # print(square)
    #
    # np.random.shuffle(squares)
    # assemble_order(squares)
    X = np.array([[569, 569, 749, 659], [810, 624, 434, 341]])
    Y = np.array([[500, 500, 400, 450], [100, 0, -100, -150]])
    A, b = get_transform_parameters(X, Y)
    print(A,b)


if __name__ == "__main__":
    main()
