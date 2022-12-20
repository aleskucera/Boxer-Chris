import os
import time

import yaml
import cv2 as cv
import PyCapture2
import numpy as np


def convert_coordinates(x: np.ndarray) -> np.ndarray:
    calib_cfg = yaml.safe_load(open('conf/calibration.yaml', 'r'))
    A = np.array(calib_cfg['matrix'])
    b = np.array(calib_cfg['vector'])[..., np.newaxis]
    return A@x + b


def set_up_camera(config: dict):
    # Load the configuration file
    # camera_cfg = yaml.safe_load(open('../conf/camera.yaml', 'r'))
    
    # Connect to the camera
    bus = PyCapture2.BusManager()
    camera = PyCapture2.Camera()
    camera.connect(bus.getCameraFromIndex(0))
    camera.startCapture()

    # Set the camera settings
    settings = config['default_settings']
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.WHITE_BALANCE, 
                       valueA=settings['white_balance_red'], valueB=settings['white_balance_blue'])
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.SHUTTER, absValue=settings['shutter'], autoManualMode=False)
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=settings['gain'], autoManualMode=False)
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.BRIGHTNESS, absValue=settings['brightness'], autoManualMode=False)

    return camera


def capture_images(camera: PyCapture2.Camera, directory: str, config: dict):

    os.makedirs(directory, exist_ok=True)

    for color, value in config['gain'].items():

        # Set the gain to the value for the current color
        camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=value, autoManualMode=False)
        time.sleep(0.1)

        # Capture the image
        image = camera.retrieveBuffer()
        image = image.convert(PyCapture2.PIXEL_FORMAT.BGR)

        # Convert the image to a numpy array
        cv_image = np.array(image.getData(), dtype="uint8").reshape((image.getRows(), image.getCols(), 3))
        image_path = os.path.join(directory, f'{color}.png')
        cv.imwrite(image_path, cv_image)

        print(f'Captured image for {color} cubes.')


def draw_squares(image: np.ndarray, squares: np.ndarray):
    for s in squares:
        cv.drawContours(image, [s.corners], 0, s.color[::-1], 3)
        cv.putText(image, f'{s.center}', s.corners[0],
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv.LINE_AA)
    # Display the squares
    cv.imshow('image', image)
    cv.waitKey(0)

