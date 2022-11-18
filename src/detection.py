import cv2
import yaml
import numpy as np
from dataclasses import dataclass


@dataclass
class Square:
    x: float
    y: float
    width: float
    height: float
    rotation: float
    contour: np.ndarray
    corners: np.ndarray

    @property
    def area(self):
        return self.width * self.height

    @property
    def center(self):
        return self.x, self.y


def detect_squares(image: np.ndarray, color: str, config_file: str) -> tuple:
    # Load configuration
    cfg = yaml.safe_load(open(config_file, 'r'))
    limits = cfg['limits'][color]
    lower = tuple(limits['lower'])
    upper = tuple(limits['upper'])

    # ------------------ Filter inside squares ------------------

    # Edge detection
    gray_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 50, 120) # 50, 100

    # Morphology closing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Apply mask
    mask = cv2.threshold(closing, 127, 255, cv2.THRESH_BINARY_INV)[1]
    image_f1 = cv2.bitwise_and(image, image, mask=mask)

    # ------------------ Filter color ------------------

    # Filter color based od HSV limits
    hsv_img = cv2.cvtColor(image_f1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower, upper)
    image_f2 = cv2.bitwise_and(image_f1, image_f1, mask=mask)

    # Threshold image
    thresh = threshold(image_f2, limits['threshold'])

    # ------------------ Detect squares ------------------

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter squares
    squares = filter_squares(contours)

    return edges, image_f1, image_f2, thresh, contours, squares


def filter_squares(contours, min_area: float = 1000, max_ratio: float = 0.2) -> list:
    squares = []
    for contour in contours:

        # Approximate contour to polygon
        approx = cv2.approxPolyDP(contour, 0.06 * cv2.arcLength(contour, True), True)

        # Skip if contour is not a rectangle
        if len(approx) == 4:
            # Approximate rectangle properties
            rectangle = cv2.minAreaRect(contour)
            corners = cv2.boxPoints(rectangle)
            corners = np.int0(corners)

            ((x, y), (width, height), rotation) = rectangle

            # Skip if rectangle isn't similar to square or is too small
            if width * height > min_area and abs(width - height) / (width + height) < max_ratio:
                square = Square(x, y, width, height, rotation, contour, corners)
                squares.append(square)
    return squares


def threshold(image: np.ndarray, threshold: int, open_kernel: tuple = (3, 3),
              close_kernel: tuple = (30, 30)) -> np.ndarray:
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    kernel = np.ones(open_kernel, np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = np.ones(close_kernel, np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return thresh
