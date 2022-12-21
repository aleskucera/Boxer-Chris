import os
import time

import yaml
import cv2 as cv
import PyCapture2
import numpy as np

from src import calibrate, robCRS97, Commander, set_up_camera, robCRSgripper, move_cube, CubePosition, capture_images, detect_squares, move

def convert_coordinates(x: int, y: int) -> np.ndarray:
    v = np.array([[x], [y]])
    calib_cfg = yaml.safe_load(open('conf/calibration.yaml', 'r'))
    A = np.array(calib_cfg['matrix'])
    b = np.array(calib_cfg['vector'])[..., np.newaxis]
    return A@v + b


def main():
    calib_cfg = yaml.safe_load(open('conf/calibration.yaml', 'r'))
    camera_cfg = yaml.safe_load(open('conf/camera.yaml', 'r'))
    detection_cfg = yaml.safe_load(open('conf/detection.yaml', 'r'))
    motion_cfg= yaml.safe_load(open('conf/motion.yaml', 'r'))

    robot = robCRS97()
    tty_dev = '/dev/ttyUSB0'
    commander = Commander(robot)
    commander.open_comm(tty_dev, speed=19200)

    camera = set_up_camera(camera_cfg)

    commander.init(reg_type=None, max_speed=None, hard_home=False)
    robCRSgripper(commander, -1)
    commander.wait_ready()

    # calibrate(commander, camera, calib_cfg, camera_cfg, detection_cfg)
    p0 = CubePosition(500, -290, 0)
    p1 = CubePosition(500, 0, 0)
    move_cube(commander, p0, p1, motion_cfg, center_dest=False)
    # move(commander, [300, -190, 300, 0, 90, 0], [300, 190, 300, 0, 90, 0])

    # capture_images(camera, 'camera/images/', camera_cfg)
    # image_path = os.path.join('camera/images/', 'red.png')
    # image = cv.imread(image_path)
    # squares = detect_squares('camera/images/', image, detection_cfg)
    # print(squares)

    # bigger_square, middle_square, smaller_square = sorted(squares, reverse=True)

    # s = convert_coordinates(smaller_square.x, smaller_square.y)
    # m = convert_coordinates(middle_square.x, middle_square.y)
    # b = convert_coordinates(bigger_square.x, bigger_square.y)

    # ps = CubePosition(s[0], s[1], smaller_square.angle)
    # pm = CubePosition(m[0], m[1], middle_square.angle)
    # pb = CubePosition(b[0], b[1], bigger_square.angle)
    
    # move_cube(commander, pm, pb)

    # capture_images(camera, 'camera/images/', camera_cfg)
    # image_path = os.path.join('camera/images/', 'red.png')
    # image = cv.imread(image_path)
    # squares = detect_squares('camera/images/', image, detection_cfg)

    # middle_square, smaller_square = sorted(squares, reverse=True)

    # s = convert_coordinates(smaller_square.x, smaller_square.y)
    # m = convert_coordinates(middle_square.x, middle_square.y)

    # ps = CubePosition(s[0], s[1], smaller_square.angle)
    # pm = CubePosition(m[0], m[1], middle_square.angle)

    # move_cube(commander, ps, pm)

    # print(f'CAMERA - x: {squares[0].x}, y: {squares[0].y}')

    # y = convert_coordinates(squares[0].x, squares[0].y)
    # print(y)
    # print(f'GLOBAL - x: {y[0]}, y: {y[1]}')
    
    

if __name__ == '__main__':
    main()