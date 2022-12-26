import cv2 as cv
import numpy as np
import random
import yaml

from src.detection import detect_squares
from src.objects import Cube


def split_cubes_by_size(cubes):
    """ Split cubes by size
    :param cubes: array of cubes
    :return: cubes split into arrays by size
    """
    sizes = np.array([cube.id for cube in cubes])
    sizes = np.sort(np.unique(sizes))[::-1]
    cubes_by_size = []
    for size in sizes:
        cubes_by_size.append([])
        for cube in cubes:
            if cube.id == size:
                cubes_by_size[-1].append(cube)
    return np.array(cubes_by_size, dtype=object)


def get_cubes2stack(cubes: np.ndarray, color_priority: bool, already_stacked=[], last_id=10) -> np.ndarray:
    """ Get cubes to stack
    :param cubes: array of cubes
    :param color_priority: if True, cubes will be stacked primarily by color
    :param already_stacked: array of cubes that cannot be taken as small again (they are already in bigger cube)
    :return: array of all cubes in order to stack
    """
    small_cube = None
    big_cube = None
    if last_id == 0:
        last_id = 10
    if color_priority:
        # TODO: will be implemented later
        pass
    else:
        cubes_by_size = split_cubes_by_size(cubes)
        cubes_by_size_and_color = sort_cubes_by_color(cubes_by_size)
        while True:
            small_cube, big_cube, last_id = choose_big_and_small_cube(cubes_by_size_and_color, already_stacked, last_id)
            if small_cube is None and big_cube is not None:
                idx = np.where(cubes_by_size_and_color == big_cube)
                cubes = np.delete(cubes, idx)
                cubes_by_size = split_cubes_by_size(cubes)
                cubes_by_size_and_color = sort_cubes_by_color(cubes_by_size)
            else:
                break
    return small_cube, big_cube, already_stacked, last_id


def choose_big_and_small_cube(cubes_by_size_and_color: np.ndarray, already_stacked: list, last_id) -> (Cube, Cube):
    """ Choose big and small cube to stack
    :param cubes_by_size_and_color: array of cubes split by size and then sorted by color
    :param already_stacked: array of cubes that cannot be taken as small again (they are already in bigger cube)
    :last_id: size of the last small cube
    :return: (big cube, small cube) -> (None, None) if there are no cubes to stack
    """
    small_cube = None
    big_cube = None
    for size_category in cubes_by_size_and_color:
        for cube in size_category:
            if big_cube is None and last_id >= cube.id:
                big_cube = cube
                break
            if small_cube is None and big_cube is not None and cube not in already_stacked:
                small_cube = cube
                last_id = small_cube.id
                already_stacked.append(small_cube)
                break
    return small_cube, big_cube, last_id


def sort_cubes_by_color(cubes_by_size):
    """ Sort cubes by color
    :param cubes_by_size: array of cubes split by size
    :return: array of cubes split by size and sorted by color
    """
    cubes_by_size_and_color = []
    for size_category in cubes_by_size:
        category_by_color = sorted(
            size_category,
            key=lambda cube: cube.color,
            reverse=True
        )
        cubes_by_size_and_color.append(category_by_color)
    return np.array(cubes_by_size_and_color, dtype=object)


def print_cubes(cubes):
    print("________________________________")
    for cube in cubes:
        print(cube)
    print("________________________________")


def main():
    cubes = []
    colors = np.array(["black", "blue", "green", "red", "yellow", "orange"])

    motion_cfg = yaml.safe_load(open('../conf/motion.yaml', 'r'))

    n = 3

    for i in range(n):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        angle = random.randint(0, 90)
        size_id = random.randint(2, 6)
        color = np.random.choice(colors)
        cubes.append(Cube(x, y, angle, size_id, motion_cfg, color))

    cubes = np.array(cubes)

    while True:
        print("________________________________")
        print("NEW ITERATION")
        print("CUBES ON TABLE:")
        print_cubes(cubes)
        smaller_cube, bigger_cube, already_stacked, last_id = get_cubes2stack(cubes, False)
        print("ALREADY STACKED:")
        print(already_stacked)
        print("BIG CUBE:")
        print(bigger_cube)
        print("SMALL CUBE:")
        print(smaller_cube)
        if bigger_cube is not None:
            cubes = np.delete(cubes, np.where(cubes == bigger_cube))
        if smaller_cube is None and bigger_cube is None:
            break


if __name__ == '__main__':
    main()
