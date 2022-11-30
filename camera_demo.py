import PyCapture2
import cv2
import numpy as np
from datetime import datetime
import time

bus = PyCapture2.BusManager()
camera = PyCapture2.Camera()

camera.connect(bus.getCameraFromIndex(0))
camera.startCapture()

cam_gain = camera.getProperty(PyCapture2.PROPERTY_TYPE.GAIN)
print(cam_gain.absValue)

camera.setProperty()

while True:

    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=2.0)

    cam_gain = camera.getProperty(PyCapture2.PROPERTY_TYPE.GAIN)
    print(cam_gain.absValue)

    time.sleep(1)

    camera.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=4.0)

    cam_gain = camera.getProperty(PyCapture2.PROPERTY_TYPE.GAIN)
    print(cam_gain.absValue)
    time.sleep(1)

    image = camera.retrieveBuffer()
    image = image.convert(PyCapture2.PIXEL_FORMAT.BGR)
    rgb_cv_image = np.array(image.getData(), dtype="uint8").reshape((image.getRows(), image.getCols(), 3))
    bgr_cv_image = cv2.cvtColor(rgb_cv_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('image', rgb_cv_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        now = datetime.now()
        cv2.imwrite('imgs_for_our_dear_Ales/' + now.strftime("%d-%m-%Y_%H-%M-%S") + '.png', bgr_cv_image)
        break