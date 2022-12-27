import os
import itertools

import cv2 as cv
import numpy as np
from sklearn.cluster import DBSCAN

from .objects import ApproxPolygon, Square

MAX_COS = 0.05
MAX_LEN_RATIO = 1.05

STEP = 2
MIN_THRESHOLD = 0
MAX_THRESHOLD = 255

DB_EPSILON = 3
DB_MIN_SAMPLES = 1


def detect_squares(directory: str, config: dict):
    """Detects squares in the given directory and returns a list of Square objects
    :param directory: Directory containing images of the cubes
    :param main_image: Image for which the color of the squares will be detected
    :param config: Configuration file
    """
    contours, squares = [], []

    # Find contours
    contours = find_contours(directory, MIN_THRESHOLD, MAX_THRESHOLD, STEP)
    # contours = find_contours_laplacian(directory)

    # Filter out contours that are not squares and cluster them
    labels, vectors = cluster_square_contours(contours)

    contours = vectors.reshape(-1, 4, 1, 2)

    # Create Square objects
    for i in range(np.max(labels) + 1):
        tmp = contours[labels == i]
        idx = np.argmin([cv.contourArea(c) for c in tmp])
        # mean = np.mean(contours[labels == i], axis=0, dtype=np.int32)
        squares.append(Square(tmp[idx]))

    # Filter out squares that are inside other squares
    squares = filter_outers(squares)

    # Find color of each square
    squares = assign_attributes(squares, directory, config)
    return squares


def angle_cos(p0, p1, p2) -> float:
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def max_cos(contour: np.ndarray) -> float:
    contour = contour.reshape(-1, 2)
    c, c1, c2 = contour, np.roll(contour, 1, axis=0), np.roll(contour, 2, axis=0)

    cos_angles = [angle_cos(c[i], c1[i], c2[i]) for i in range(4)]
    return max(cos_angles)


def find_contours_laplacian(directory: str) -> list:
    contours = []
    for file in os.scandir(directory):
        img = cv.imread(file.path)

        # Apply bilateral filter to reduce noise
        img = cv.bilateralFilter(img, 50, 15, 15)
        img = cv.GaussianBlur(img, (5, 5), 0)

        for channel in cv.split(img):
            # Apply Laplacian filter
            laplacian = cv.Laplacian(channel, 10, cv.CV_64F)
            laplacian = np.uint8(np.absolute(laplacian))

            # Find contours
            new_contours, _ = cv.findContours(laplacian, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            contours.extend(new_contours)

    return contours


def find_contours(directory: str, lower: int, upper: int, step: int) -> list:
    """Finds contours in the given directory
    :param directory: Directory containing images of the cubes
    :param lower: Lower threshold
    :param upper: Upper threshold
    :param step: Step size for threshold
    """
    contours = []
    # for file in os.scandir(directory):
    file = os.path.join(directory, 'red.png')
    img = cv.imread(file)
    img = cv.bilateralFilter(img, 10, 5, 5)
    img = cv.bilateralFilter(img, 20, 10, 10)
    img = cv.bilateralFilter(img, 30, 20, 20)
    img = cv.bilateralFilter(img, 30, 30, 30)
    img = cv.bilateralFilter(img, 20, 40, 40)

    cv.imshow(str(file), img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    for channel in cv.split(img):
        for threshold in range(lower, upper, step):
            _, thresh = cv.threshold(channel, threshold, 255, cv.THRESH_BINARY)
            new_contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            contours.extend(new_contours)

    return contours


def cluster_square_contours(contours: list, eps: int = DB_EPSILON,
                            min_samples: int = DB_MIN_SAMPLES) -> tuple:
    """Clusters contours that are squares
    :param contours: Contours to cluster
    :param eps: DBSCAN epsilon
    :param min_samples: DBSCAN min_samples
    """
    vectors = []
    for contour in contours:
        poly = ApproxPolygon(contour)
        if poly.area_in_range(min_area=1000, max_area=100000) and \
                poly.is_square(max_cos=MAX_COS, max_len_ratio=MAX_LEN_RATIO):
            vectors.append(poly.polygon.reshape(8, ))

    vectors = np.array(vectors)
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(vectors)

    return clustering.labels_, vectors


def filter_outers(squares: list) -> list:
    """Filters out squares that are outside the other squares
    :param squares: List of Square objects
    """
    for s1, s2 in itertools.combinations(squares, 2):
        if s1.is_inside((s2.x, s2.y)) or s2.is_inside((s1.x, s1.y)):
            if s1 > s2:
                s1.outer_square = True
            else:
                s2.outer_square = True

    return [square for square in squares if not square.outer_square]


def assign_attributes(squares: list, img_dir: str ,config: dict) -> list:
    """Assigns attributes to the squares
    :param squares: List of Square objects
    :param img_dir: image directory
    :param config: Configuration file
    """
    
    images = []
    for value in config['colors'].values():
        # image_path = os.path.join(img_dir, str(value['color']) + '.png')
        image_path = os.path.join(img_dir, str('yellow') + '.png')
        image = cv.imread(image_path)
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        images.append(hsv_image)

    for square in squares:
        colors = []

        # Find out which color is the most dominant
        for i, color in config['colors'].items():
            hsv_image = images[i]

            # Focus on the inner part of the square
            mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)
            cv.drawContours(mask, [square.corners], -1, 255, -1)
            square_hsv = cv.bitwise_and(hsv_image, hsv_image, mask=mask)
        
            lower = np.array(color['lower'])
            upper = np.array(color['upper'])

            filtered_image = cv.inRange(square_hsv, lower, upper)
            colors.append(np.sum(filtered_image))

        square.vis_color = config['colors'][np.argmax(colors)]['rgb']
        square.symbol = config['colors'][np.argmax(colors)]['symbol']
        square.color = config['colors'][np.argmax(colors)]['color']

        boundaries = config['boundaries']

        for i, (ub, lb) in enumerate(zip(boundaries['upper'], boundaries['lower'])):
            if lb < square.area < ub:
                square.id = i
    return squares
