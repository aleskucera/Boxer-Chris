import PyCapture2
import cv2
import numpy as np
from datetime import datetime
import time
import yaml
import os

with open("conf/colors.yaml", 'r') as stream:
    config = yaml.safe_load(stream)
    settings = config['default_settings']
    gain = config['gain']


bus = PyCapture2.BusManager()
camera = PyCapture2.Camera()

camera.connect(bus.getCameraFromIndex(0))
camera.startCapture()

# camera.setProperty(type=PyCapture2.PROPERTY_TYPE.BRIGHTNESS, absValue=settings['brightness'])
# camera.setProperty(type=PyCapture2.PROPERTY_TYPE.EXPOSURE, absValue=settings['exposure'])
# camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAMMA, absValue=settings['gamma'])
camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=settings['gain'])

colors = ['black', 'green', 'blue', 'red', 'orange', 'yellow']

path = 'camera/images9'
os.makedirs(path, exist_ok=True)

for color in colors:
    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=gain[color])
    time.sleep(0.5)
    image = camera.retrieveBuffer()
    image = image.convert(PyCapture2.PIXEL_FORMAT.BGR)
    rgb_cv_image = np.array(image.getData(), dtype="uint8").reshape((image.getRows(), image.getCols(), 3))
    bgr_cv_image = cv2.cvtColor(rgb_cv_image, cv2.COLOR_RGB2BGR)
    # cv2.imshow('image', rgb_cv_image)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    image_path = os.path.join(path, f'{color}.png')
    print(image_path)
    cv2.imwrite(image_path, rgb_cv_image)

