import PyCapture2
import cv2
import numpy as np
from datetime import datetime
import time
import yaml

with open("conf/colors.yaml", 'r') as stream:
    config = yaml.safe_load(stream)
    settings = config['default_settings']
    gain = settings['gain']


bus = PyCapture2.BusManager()
camera = PyCapture2.Camera()

camera.connect(bus.getCameraFromIndex(0))
camera.startCapture()

camera.setProperty(type=PyCapture2.PROPERTY_TYPE.BRIGHTNESS, absValue=settings['brightness'])
camera.setProperty(type=PyCapture2.PROPERTY_TYPE.EXPOSURE, absValue=settings['exposure'])
camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAMMA, absValue=settings['gamma'])
camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=settings['gain'])

colors = ['black', 'green', 'blue', 'yellow', 'orange', 'red']

while True:
    for color in colors:
        camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=settings[color]['gain'])
        time.sleep(1)
        image = camera.retrieveBuffer()
        image = image.convert(PyCapture2.PIXEL_FORMAT.BGR)
        rgb_cv_image = np.array(image.getData(), dtype="uint8").reshape((image.getRows(), image.getCols(), 3))
        bgr_cv_image = cv2.cvtColor(rgb_cv_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('image', rgb_cv_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            now = datetime.now()
            cv2.imwrite('camera/' + color + '.png', bgr_cv_image)
            break
    break

