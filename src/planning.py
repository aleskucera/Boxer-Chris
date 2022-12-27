import cv2 as cv
import numpy as np
import random
import yaml

from objects import Cube


def split_cubes(cubes: np.ndarray, by_size: bool) -> np.ndarray:
    """ Split cubes by size or color
    :param cubes: array of cubes
    :param by_size: if True, cubes will be split by size, otherwise by color
    :return: cubes split into arrays by the given attribute
    """

    # get attributes of all cubes
    attributes = np.array([cube.id if by_size else cube.color for cube in cubes])

    # get only the unique attributes and sort them in descending order
    sorted_attributes = np.sort(np.unique(attributes))[::-1]

    # split cubes into arrays by the attributes
    cubes_by_attribute = []
    for attribute in sorted_attributes:
        cubes_by_attribute.append(cubes[np.where(attributes == attribute)])
    return np.array(cubes_by_attribute, dtype=object)


def get_cubes2stack(cubes: np.ndarray, last_small_cube: Cube, color: str) -> tuple:
    """ Get cubes to stack
    :param cubes: array of cubes
    :param last_small_cube: last stacked small cube
    :param color: if not None, only cubes of this color will be stacked
                    (when color='all', all cubes will be stacked primarily by color)
    :return: array of all cubes in order to stack
    """

    # make sure that 'cubes' is a numpy array
    cubes = np.array(cubes)

    if color is not None:
        cubes_by_color = split_cubes(cubes, False)
        cubes_by_color_and_size = sort_categorized_cubes(cubes_by_color, True)
        small_cube, big_cube = choose_big_and_small_cube(cubes_by_color_and_size, last_small_cube, color)
    else:
        cubes_by_size = split_cubes(cubes, True)
        cubes_by_size_and_color = sort_categorized_cubes(cubes_by_size, False)
        small_cube, big_cube = choose_big_and_small_cube(cubes_by_size_and_color, last_small_cube, color)
        # while True:
        #     small_cube, big_cube = choose_big_and_small_cube(cubes_by_size_and_color, last_small_cube, color)
        #     if small_cube is None and big_cube is not None:
        #         # idx = np.where(cubes_by_size_and_color == big_cube)
        #         # cubes = np.delete(cubes, idx)
        #         delete_cube(cubes, big_cube)
        #         cubes_by_size = split_cubes(cubes, True)
        #         cubes_by_size_and_color = sort_categorized_cubes(cubes_by_size, False)
        #     else:
        #         break
    return small_cube, big_cube


def choose_big_and_small_cube(cubes_split_and_sorted: np.ndarray, last_small_cube: Cube, color: bool) -> tuple:
    """ Choose big and small cube to stack
    :param cubes_split_and_sorted: array of cubes split by one attribute and sorted by the other
    :param last_small_cube: last stacked small cube
    :param color: if not None, only cubes of this color will be stacked
                    (when color='all', all cubes will be stacked primarily by color)
    :return: (big cube, small cube) -> (None, None) if there are no cubes to stack
    """

    # initialize cubes to stack
    small_cube = None
    big_cube = None

    # get the big and the small cube
    if color is not None:
        for category in cubes_split_and_sorted:
            if len(category) > 1 and (category[0].color == color or color == 'all'):
                big_cube = category[0]
                small_cube = category[1]
                break
    else:
        for category in cubes_split_and_sorted:
            for cube in category:
                if big_cube is None and (last_small_cube is None or cube.id <= last_small_cube.id):
                    big_cube = cube
                    break
                elif big_cube is not None and cube.parent_id == cube.id:
                    small_cube = cube
                    break
            if small_cube is not None:
                break
    return small_cube, big_cube


def sort_categorized_cubes(cubes_by_attribute: np.ndarray, by_size: bool) -> np.ndarray:
    """ Sort categorized (split into sub-arrays/categories) cubes by size or color
    :param cubes_by_attribute: array of cubes split into sub-arrays/categories by an attribute
    :param by_size: if True, cubes will be sorted by size, otherwise by color
    :return: array of cubes split by an attribute and sorted by size or color
    """
    sorted_cubes = []
    for category in cubes_by_attribute:
        sorted_category = sorted(
            category,
            key=lambda cube: cube.id if by_size else cube.color,
            reverse=True
        )
        sorted_cubes.append(sorted_category)
    return np.array(sorted_cubes, dtype=object)


def delete_cube(cubes: np.ndarray, cube_to_be_deleted: Cube):
    for i in range(len(cubes)):
        for j in range(len(cubes[i])):
            if cubes[i][j] == cube_to_be_deleted:
                cubes[i] = np.delete(cubes[i], j)
                return


def print_cubes(cubes: np.ndarray):
    print("________________________________")
    for cube in cubes:
        print(cube)
    print("________________________________")


def main():
    cubes = []
    colors = np.array(["black", "blue"]) #, "green", "red", "yellow", "orange"])

    motion_cfg = yaml.safe_load(open('../conf/motion.yaml', 'r'))

    n = 6

    for i in range(n):
        while True:
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            angle = random.randint(0, 90)
            size_id = random.randint(2, 6)
            color = np.random.choice(colors)
            cube = Cube(x, y, angle, size_id, size_id, motion_cfg, color)
            if cube not in cubes:
                cubes.append(cube)
                break

    cubes = np.array(cubes)

    smaller_cube = None

    while True:
        print("________________________________")
        print("NEW ITERATION")
        print("CUBES ON TABLE:")
        print_cubes(cubes)
        smaller_cube, bigger_cube = get_cubes2stack(cubes, smaller_cube, None)
        print("CUBES TO BE STACKED:")
        print("BIG CUBE:")
        print(bigger_cube)
        print("SMALL CUBE:")
        print(smaller_cube)
        if bigger_cube is not None:
            cubes[np.where(cubes == smaller_cube)][0].parent_id = bigger_cube.id
            cubes = np.delete(cubes, np.where(cubes == bigger_cube))
        if smaller_cube is None and bigger_cube is None:
            break


if __name__ == '__main__':
    main()
