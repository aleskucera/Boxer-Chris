import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

import matplotlib

matplotlib.use('TkAgg')


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


def filter_squares(contours, min_area: float = 1000, max_ratio: float = 0.2) -> list:
    squares = []
    for contour in contours:

        # Approximate contour to polygon
        approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)

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


def process_mask(image: np.ndarray, threshold: int, open_kernel: tuple = (2, 2),
                 close_kernel: tuple = (40, 40)) -> np.ndarray:
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    kernel = np.ones(open_kernel, np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = np.ones(close_kernel, np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return thresh


def color_mask(image: np.ndarray, lower: tuple, upper: tuple) -> np.ndarray:
    hsv_img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower, upper)
    return mask


def find_contours(image: np.ndarray) -> list:
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detect_squares(image: np.ndarray, color: str) -> tuple:
    cfg = yaml.safe_load(open('../conf/hsv_limits.yaml', 'r'))
    lower = tuple(cfg[color]['lower'])
    upper = tuple(cfg[color]['upper'])
    threshold = cfg[color]['threshold']

    mask = color_mask(image.copy(), lower, upper)
    mask = cv2.bitwise_and(image, image, mask=mask)
    threshold = process_mask(mask, threshold)
    contours = find_contours(threshold)
    squares = filter_squares(contours)

    return squares, threshold, mask


def squares_demo(image: np.ndarray, color: str) -> None:
    # Detect squares
    original = image.copy()
    squares, threshold, mask = detect_squares(image, color)

    if color in ['red', 'orange', 'yellow']:
        plt_color = (112, 25, 25)
    else:
        plt_color = (175, 0, 255)

    # Plot the results
    for square in squares:
        cv2.drawContours(image, [square.contour], -1, plt_color, 3)
        cv2.circle(image, (int(square.x), int(square.y)), 8, plt_color, -1)
        for i in range(4):
            cv2.circle(image, (int(square.corners[i, 0]), int(square.corners[i, 1])), 8, plt_color, -1)

    images = [original[..., ::-1], mask[..., ::-1], threshold, image[..., ::-1]]
    titles = ['Original Image', 'Filtered Color', 'Processed Color Mask', 'Detected Squares']

    for i, img in enumerate(images):
        plt.subplot(2, 2, i + 1)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])

    plt.show()


if __name__ == '__main__':
    image = cv2.imread('../imgs_for_our_dear_Ales/1.png')
    squares_demo(image, 'orange')
