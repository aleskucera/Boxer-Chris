import os
import time

import cv2 as cv
import numpy as np

try:
    import PyCapture2
except ImportError:
    print('PyCapture2 not found')


def set_up_camera(config: dict):
    """Sets up the camera and returns a camera object
    :param config: Configuration file
    """

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


def capture_images(camera, directory: str, config: dict):
    """Captures images from the camera and saves them to the given directory
    :param camera: Camera object
    :param directory: Directory to save the images to
    :param config: Configuration file
    """
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
