import cv2
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

import matplotlib

matplotlib.use('TkAgg')

TRESHOLD = 115


@dataclass
class Square:
    x: float
    y: float
    width: float
    height: float
    rotation: float
    contour: np.ndarray

    @property
    def area(self):
        return self.width * self.height

    @property
    def center(self):
        return self.x, self.y


def treshold_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # denoise = cv2.fastNlMeansDenoising(gray, 10, 15, 7, 21)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blur, TRESHOLD, 255, cv2.THRESH_BINARY)
    # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
    return thresh


def find_contours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detect_squares(contours):
    squares = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            ((x, y), (width, height), rotation) = cv2.minAreaRect(contour)
            if abs(width - height) < 100:
                square = Square(x, y, width, height, rotation, contour)
                if square.area > 3000:
                    squares.append(square)

    return squares


def main():
    # Load image
    image = cv2.imread('../imgs_for_our_dear_Ales/5.png')[..., ::-1]

    # Threshold image
    threshold = treshold_image(image)

    # Find contours
    cnts = find_contours(threshold)
    contours_image = np.full(image.shape, 255, dtype=np.uint8)
    cv2.drawContours(contours_image, cnts, -1, (173, 1, 255), 10)

    # Detect squares
    squares = detect_squares(cnts)
    squares_image = np.full(image.shape, 255, dtype=np.uint8)
    for square in squares:
        cv2.drawContours(squares_image, [square.contour], -1, (50, 200, 0), 10)

    # Create center mask
    center_mask = np.full(image.shape, 255, dtype=np.uint8)
    for square in squares:
        cv2.circle(center_mask, (int(square.x), int(square.y)), 10, (0, 0, 0), -1)

    # Result
    result = cv2.bitwise_and(squares_image, center_mask)
    # Add text to result
    for square in squares:
        x_text = f'x: {int(square.x)}'
        cv2.putText(center_mask, x_text, (int(square.x + 20), int(square.y + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        y_text = f'y: {int(square.y)}'
        cv2.putText(center_mask, y_text, (int(square.x + 20), int(square.y + 60)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        area_text = f'a: {int(square.area):d}'
        cv2.putText(result, area_text, (int(square.x - 70), int(square.y + 40)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Plot the results
    images = [image, threshold, contours_image, squares_image, center_mask, result]
    titles = ['Original image', 'Binary Threshold', 'Contour Detection', 'Square Filtration', 'Center Mask', 'Result']

    for i, img in enumerate(images):
        plt.subplot(2, 3, i + 1)
        plt.imshow(img, 'gray')
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])

    plt.show()


if __name__ == '__main__':
    main()
