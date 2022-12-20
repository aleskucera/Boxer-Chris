import os
import time

import yaml
import cv2 as cv
import PyCapture2
import numpy as np

from src import calibrate, robCRS97, Commander, set_up_camera, robCRSgripper

def main():
    calib_cfg = yaml.safe_load(open('conf/calibration.yaml', 'r'))
    camera_cfg = yaml.safe_load(open('conf/camera.yaml', 'r'))
    detection_cfg = yaml.safe_load(open('conf/detection.yaml', 'r'))

    robot = robCRS97()
    tty_dev = '/dev/ttyUSB0'
    commander = Commander(robot)
    commander.open_comm(tty_dev, speed=19200)

    camera = set_up_camera(camera_cfg)

    # commander.init(reg_type=None, max_speed=None, hard_home=True)
    # robCRSgripper(commander, -1)
    # commander.wait_ready()


    calibrate(commander, camera, calib_cfg, camera_cfg, detection_cfg)

if __name__ == '__main__':
    main()