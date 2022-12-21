import os
from copy import deepcopy

import cv2 as cv
import numpy as np
from scipy.optimize import least_squares

from .objects import Cube
from .image import capture_images
from .CRS_commander import Commander
from .detection import detect_squares
from .motion import center_cube, move_cube


def calibrate(commander: Commander, camera, calib_config: dict, camera_config: dict,
              detection_cfg: dict, motion_config: dict) -> None:
    """Calibrate camera to robot transformation
    :param commander: Commander object
    :param camera: PyCapture2 camera object
    :param calib_config: calibration configuration
    :param camera_config: camera configuration
    :param detection_cfg: detection configuration
    :param motion_config: motion configuration
    """

    # Load calibration config
    base_position = calib_config["base_position"]
    positions = calib_config["positions"]

    # Center cube at initial position
    p = Cube(base_position['x'], base_position['y'], 0, 6, motion_config)
    center_cube(commander, p)

    initial_positions = [base_position] + positions
    end_positions = np.roll(initial_positions, -1, axis=0)

    camera_coords = []
    for ip, ep in zip(initial_positions, end_positions):
        p0, p1 = deepcopy(p), deepcopy(p)
        p0.x, p0.y = ip['x'], ip['y']
        p1.x, p1.y = ep['x'], ep['y']
        move_cube(commander, p0, p1, motion_config['base_position'], center_dest=False)

        # Capture images
        capture_images(camera, camera_config['img_directory'], camera_config)
        image_path = os.path.join(camera_config['img_directory'], 'red.png')
        image = cv.imread(image_path)

        # Detect squares
        squares = detect_squares(camera_config['img_directory'], image, detection_cfg)

        if len(squares) == 1:
            camera_coords.append([squares[0].x, squares[0].y])

        cv.drawContours(image, [squares[0].corners], 0, squares[0].color[::-1], 3)
        cv.imwrite('output.png', image)

    camera_coords = np.array(camera_coords).T

    global_coords = [[p['x'], p['y']] for p in end_positions]
    global_coords = np.array(global_coords).T

    A, b = get_transform_parameters(camera_coords, global_coords)
    print(f'A: {A}')
    print(f'b: {b}')

    # Save transform parameters
    np.savez('conf/transform.npz', A=A, b=b)


def optimized_func(x, cam, glob):
    a11, a21, a12, a22, b1, b2 = x
    x_cam = cam[0, :]
    y_cam = cam[1, :]

    x_glob = glob[0, :]
    y_glob = glob[1, :]

    ones = np.ones_like(x_cam)

    f1 = a11 * x_cam + a12 * y_cam + ones * b1 - x_glob
    f2 = a21 * x_cam + a22 * y_cam + ones * b2 - y_glob

    return np.hstack((f1, f2))


def get_transform_parameters(X, Y):
    x0 = [1, 0, 0, 1, 0, 0]
    x = least_squares(optimized_func, x0, args=(X, Y)).x
    a11, a21, a12, a22, b1, b2 = x

    return np.array([[a11, a12], [a21, a22]]), np.array([[b1], [b2]])
