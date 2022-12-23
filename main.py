import os
import time
from copy import deepcopy

import yaml
import cv2 as cv
import numpy as np

from src import calibrate, robCRS97, Commander, set_up_camera, robCRSgripper, move_cube, detect_squares, Cube, \
    center_cube, capture_images, visualize_squares

calib_cfg = yaml.safe_load(open('conf/calibration.yaml', 'r'))
camera_cfg = yaml.safe_load(open('conf/camera.yaml', 'r'))
detection_cfg = yaml.safe_load(open('conf/detection.yaml', 'r'))
motion_cfg = yaml.safe_load(open('conf/motion.yaml', 'r'))

transformation = np.load('conf/transformation.npz')
A = transformation['A']
b = transformation['b']

base_position = {'x': 500, 'y': -290}
dest_position = {'x': 500, 'y': -100}
test_cube = Cube(base_position['x'], base_position['y'], 0, 6, motion_cfg)


# def convert_coordinates(x: int, y: int) -> np.ndarray:
#     v = np.array([[x], [y]])
#     calib_cfg = yaml.safe_load(open('conf/calibration.yaml', 'r'))
#     A = np.array(calib_cfg['matrix'])
#     b = np.array(calib_cfg['vector'])[..., np.newaxis]
#     return A @ v + b


def detection_demo(directory: str, mode: str):
    """
    :param directory: directory of images
    :param mode: 'centers', 'areas', 'ids' or 'images'
    """
    image_path = os.path.join(directory, 'red.png')
    image = cv.imread(image_path)
    squares = detect_squares(directory, image, detection_cfg)
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


def test_transformation(hard_home: bool = False):
    """Test transformation matrix and vector from camera to robot
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
    

    # Center cube at initial position
    # center_cube(commander, test_cube)

    # # Capture images
    # capture_images(camera, camera_cfg['img_directory'], camera_cfg)
    # image_path = os.path.join(camera_cfg['img_directory'], 'red.png')
    # image = cv.imread(image_path)
    # squares = detect_squares(camera_cfg['img_directory'], image, detection_cfg)

    # # Visualize detected square
    # visualize_squares(image, squares, 'centers')

    # Move cube to the destination position
    dest_cube = deepcopy(test_cube)
    dest_cube.x, dest_cube.y = dest_position['x'], dest_position['y']
    move_cube(commander, test_cube, dest_cube, motion_cfg['off_screen_position'], center_dest=False)

    # Visualize detected square
    # visualize_squares(image, squares, 'centers')


def demo_two_cubes(hard_home: bool = False):
    """Put two cubes into each other
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

    while(True):
        # Capture images
        capture_images(camera, camera_cfg['img_directory'], camera_cfg)
        image_path = os.path.join(camera_cfg['img_directory'], 'red.png')
        image = cv.imread(image_path)
        squares = detect_squares(camera_cfg['img_directory'], image, detection_cfg)

        # Visualize detected square
        visualize_squares(image, squares, 'ids')
        squares.sort()

        # Create cube objects
        cubes = [square.create_cube(A, b, motion_cfg) for square in squares]

        # sort cubes
        # cubes.sort()

        if len(cubes) == 1:
           return 

        # Move cube to the destination position
        move_cube(commander, cubes[-2], cubes[-1],  motion_cfg['off_screen_position'])


def main():
    # detection_demo('camera/images2/', 'ids')
    demo_two_cubes(True)
    # test_transformation(False)


if __name__ == '__main__':
    main()
