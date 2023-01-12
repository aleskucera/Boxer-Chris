import os

import yaml
import cv2 as cv
import numpy as np

from src import calibrate, robCRS97, Commander, set_up_camera, robCRSgripper, move_cube, \
    detect_squares, Cube, capture_images, visualize_squares, get_cubes2stack

calib_cfg = yaml.safe_load(open('conf/calibration.yaml', 'r'))
camera_cfg = yaml.safe_load(open('conf/camera.yaml', 'r'))
detection_cfg = yaml.safe_load(open('conf/detection.yaml', 'r'))
motion_cfg = yaml.safe_load(open('conf/motion.yaml', 'r'))

transformation = np.load('conf/transform_test.npz')
A = transformation['A']
b = transformation['b']

base_position = {'x': 500, 'y': -290}
dest_position = {'x': 500, 'y': -100}
test_cube = Cube(base_position['x'], base_position['y'], 0, 6, 6, motion_cfg)


def detection_demo(directory: str, mode: str):
    """
    :param directory: directory of images
    :param mode: 'centers', 'areas', 'ids' or 'images'
    """

    camera = set_up_camera(camera_cfg)
    
    capture_images(camera, directory, camera_cfg)

    image_path = os.path.join(directory, 'dark.png')
    image = cv.imread(image_path)

    squares = detect_squares(directory, detection_cfg)

    visualize_squares(image, squares, mode)


def get_transformation(hard_home: bool = False):
    """Get transformation matrix and vector from camera to robot
    :param hard_home: if True, robot will be homed before calibration
    """
    robot = robCRS97()
    tty_dev = '/dev/ttyUSB0'
    commander = Commander(robot)
    commander.open_comm(tty_dev, speed=19200)

    camera = set_up_camera(camera_cfg)

    robCRSgripper(commander, -1)
    commander.wait_gripper_ready()
    commander.init(reg_type=None, max_speed=None, hard_home=hard_home)

    calibrate(commander, camera, calib_cfg, camera_cfg, detection_cfg, motion_cfg)


def cube_insertion(hard_home: bool = False, mode: str = 'all'):

    # Initialize robot
    robot = robCRS97()
    tty_dev = '/dev/ttyUSB0'
    commander = Commander(robot)
    commander.open_comm(tty_dev, speed=19200)

    robCRSgripper(commander, -1)
    commander.wait_gripper_ready()
    commander.init(reg_type=None, max_speed=None, hard_home=hard_home)

    # Initialize camera
    camera = set_up_camera(camera_cfg)

    # Detect squares
    capture_images(camera, camera_cfg['img_directory'], camera_cfg)
    squares = detect_squares(camera_cfg['img_directory'], detection_cfg)
    init_squares = {(square.id, square.color): square.id for square in squares}

    small_cube = None

    while True:
        # Capture images
        capture_images(camera, camera_cfg['img_directory'], camera_cfg)

        # detect squares in the images
        squares = detect_squares(camera_cfg['img_directory'], detection_cfg)

        # Assign ids to squares
        for square in squares:
            if (square.id, square.color) in init_squares:
                square.parent_id = init_squares[(square.id, square.color)]

        # Visualize squares
        image_path = os.path.join(camera_cfg['img_directory'], 'dark.png')
        image = cv.imread(image_path)
        visualize_squares(image, squares, 'parents')

        # Create cube objects and filter out unreachable cubes
        cubes = [square.create_cube(A, b, motion_cfg) for square in squares]
        print('Number of detected cubes: ', len(cubes))

        not_identified_cubes = [cube for cube in cubes if not cube.is_identified()]
        print('Number of not identified cubes (removing): ', len(not_identified_cubes))

        not_reachable_cubes = [cube for cube in cubes if not cube.is_reachable(commander)]
        print('Cubes not reachable (removing): ', not_reachable_cubes)

        smallest_cubes = [cube for cube in cubes if cube.id == 0]
        print('Smallest cubes (removing): ', smallest_cubes)

        valid_cubes = [cube for cube in cubes if
                       cube not in not_reachable_cubes and
                       cube not in not_identified_cubes and
                       cube not in smallest_cubes]

        # valid_cubes = [cube for cube in cubes if (cube.is_reachable(commander) and cube.is_identified())]

        # Get small and big cube for insertion
        small_cube, big_cube = get_cubes2stack(valid_cubes, small_cube, mode)

        if small_cube is None or big_cube is None:
            break

        # Change small cube parent id to big cube id
        init_squares[(small_cube.id, small_cube.color)] = big_cube.parent_id

        # Insert small cube into big cube
        move_cube(commander, small_cube, big_cube,  motion_cfg['off_screen_position'])


def main():
    # detection_demo('camera/test', 'ids')
    cube_insertion(False, None)
    # get_transformation(False)


if __name__ == '__main__':
    main()
