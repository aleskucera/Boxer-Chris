import os
import time
import itertools

import yaml
import cv2 as cv
import numpy as np
from sklearn.cluster import DBSCAN

IMAGE_NUMBER = 8

MIN_AREA = 1000
MAX_AREA = 100000

MAX_COS = 0.05
MAX_LEN_RATIO = 1.08

MIN_THRESHOLD = 0
MAX_THRESHOLD = 255
STEP = 5

DP_EPSILON = 0.05

DB_EPSILON = 5
DB_MIN_SAMPLES = 2


class ApproxPolygon:
    def __init__(self, contour):
        self.length = cv.arcLength(contour, True)
        self.polygon = cv.approxPolyDP(contour, DP_EPSILON * self.length, True).reshape(-1, 2)
        self.area = cv.contourArea(self.polygon)

    def area_in_range(self, min_area=MIN_AREA, max_area=MAX_AREA):
        return min_area < self.area < max_area

    def is_square(self, max_cos=MAX_COS, max_len_ratio=MAX_LEN_RATIO):
        if len(self.polygon) == 4 and cv.isContourConvex(self.polygon):
            c, c1, c2 = self.polygon, np.roll(self.polygon, 1, axis=0), np.roll(self.polygon, 2, axis=0)

            lengths = [np.sqrt((c[i][0] - c1[i][0]) ** 2 + (c[i][1] - c1[i][1]) ** 2) for i in range(4)]
            cos_angles = [self.angle_cos(c[i], c1[i], c2[i]) for i in range(4)]

            if max(cos_angles) < max_cos and max(lengths) / min(lengths) < max_len_ratio:
                return True

        return False

    @staticmethod
    def angle_cos(p0, p1, p2):
        d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
        return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


class Square:
    def __init__(self, contour, color=None):
        self.id = None
        self.color = color
        self.symbol = None
        self.color_name = None

        rect = cv.minAreaRect(contour)
        self.corners = cv.boxPoints(rect).astype(int)

        (x, y), (w, h), angle = rect

        self.area = w * h
        self.angle = -angle
        self.width = int(w)
        self.height = int(h)
        self.center = (int(x), int(y))

        self.outer_square = None

    def is_inside(self, point: tuple):
        point = tuple(map(float, point))
        return cv.pointPolygonTest(self.corners, point, False) > 0

    def __lt__(self, other):
        return self.area < other.area

    def __gt__(self, other):
        return self.area > other.area

    def __eq__(self, other):
        return self.area == other.area

    def __ne__(self, other):
        return self.area != other.area


def detect_squares(directory: str, main_image: np.ndarray, config: dict):
    contours, squares = [], []

    hsv_image = cv.cvtColor(main_image, cv.COLOR_BGR2HSV)

    # Find contours
    contours = find_contours(directory, MIN_THRESHOLD, MAX_THRESHOLD, STEP)

    # Filter out contours that are not squares and cluster them
    labels, vectors = cluster_square_contours(contours)

    # Create Square objects
    for i in range(np.max(labels) + 1):
        mean = np.mean(vectors[labels == i], axis=0, dtype=np.int32).reshape(4, 2)
        squares.append(Square(mean))

    # Filter out squares that are inside other squares
    squares = filter_outers(squares)

    # Find colors of squares
    squares = assign_color(squares, hsv_image, config)
    return squares


def find_contours(directory: str, lower: int, upper: int, step: int) -> list:
    contours = []
    for file in os.scandir(directory):
        img = cv.imread(file.path)

        # Find squares in every color channel
        for channel in cv.split(img):
            for threshold in range(lower, upper, step):
                _retval, thresh = cv.threshold(channel, threshold, 255, cv.THRESH_BINARY)
                cnts, _hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
                contours.extend(cnts)

    return contours


def cluster_square_contours(contours: list, eps: int = DB_EPSILON,
                            min_samples: int = DB_MIN_SAMPLES) -> tuple[np.ndarray, np.ndarray]:
    vectors = []

    for contour in contours:
        poly = ApproxPolygon(contour)
        if poly.area_in_range() and poly.is_square():
            vectors.append(poly.polygon.reshape(8, ))

    vectors = np.array(vectors)
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(vectors)

    return clustering.labels_, vectors


def filter_outers(squares: list) -> list:
    for s1, s2 in itertools.combinations(squares, 2):
        if s1.is_inside(s2.center) or s2.is_inside(s1.center):
            if s1 > s2:
                s1.outer_square = True
            else:
                s2.outer_square = True

    return [square for square in squares if not square.outer_square]


def assign_color(squares: list, hsv_image: np.ndarray, config: dict) -> list:
    for square in squares:
        colors = []

        # Focus on the inner part of the square
        mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)
        cv.drawContours(mask, [square.corners], -1, 255, -1)
        square_hsv = cv.bitwise_and(hsv_image, hsv_image, mask=mask)

        # Find out which color is the most dominant
        for color in config['colors'].values():
            lower = np.array(color['lower'])
            upper = np.array(color['upper'])

            filtered_image = cv.inRange(square_hsv, lower, upper)
            colors.append(np.sum(filtered_image))

        square.color = config['colors'][np.argmax(colors)]['rgb']
        square.symbol = config['colors'][np.argmax(colors)]['symbol']

    return squares


if __name__ == '__main__':
    cfg = yaml.safe_load(open('../conf/main.yaml', 'r'))
    img = cv.imread(f'../camera/images{IMAGE_NUMBER}/red.png')

    start = time.time()
    square_list = detect_squares(f'../camera/images{IMAGE_NUMBER}', img, cfg)
    end = time.time()

    print(f'Found {len(square_list)} squares in {end - start} seconds')

    for s in square_list:
        cv.drawContours(img, [s.corners], 0, s.color[::-1], 3)

        cv.putText(img, f'{int(-s.angle)}', (int(s.center[0] - 10), int(s.center[1] + 10)),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, s.color[::-1], 2, cv.LINE_AA)

    cv.imwrite(f'../output/image{IMAGE_NUMBER}.png', img)
    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
