import os
import time

import yaml
import cv2 as cv
import PyCapture2
import numpy as np

from src import detect_squares

def capture_images(camera: PyCapture2.Camera, directory: str, config: dict):
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

    print(f'Captured images and saved the to {directory}')

def main():
    # Load the configuration file
    camera_cfg = yaml.safe_load(open('conf/camera.yaml', 'r'))
    detection_cfg = yaml.safe_load(open('conf/detection.yaml', 'r'))

    # Create the directory to save the images
    directory = 'camera/images'
    
    os.makedirs(directory, exist_ok=True)

    # Connect to the camera
    bus = PyCapture2.BusManager()
    camera = PyCapture2.Camera()
    camera.connect(bus.getCameraFromIndex(0))
    camera.startCapture()

    # Set the camera settings
    settings = camera_cfg['default_settings']
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.WHITE_BALANCE, valueA=settings['white_balance_red'], valueB=settings['white_balance_blue'])
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.SHUTTER, absValue=settings['shutter'], autoManualMode=False)
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=settings['gain'], autoManualMode=False)
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.BRIGHTNESS, absValue=settings['brightness'], autoManualMode=False)

    # Capture the images
    capture_images(camera, directory, camera_cfg)
    image = cv.imread('camera/images/red.png')


    # Detect the squares
    squares = detect_squares(directory, image, detection_cfg)

    for s in squares:
        cv.drawContours(image, [s.corners], 0, s.color[::-1], 3)

        print(s.corners.shape)
        cv.putText(image, f'{s.center}', s.corners[0],
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv.LINE_AA)

        print(f'{s.center}: {s.angle}')

    # Display the squares
    cv.imshow('image', image)
    cv.waitKey(0)

if __name__ == '__main__':
    main()




