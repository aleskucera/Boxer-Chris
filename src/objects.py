import cv2 as cv
import numpy as np


class ApproxPolygon:
    def __init__(self, contour: np.ndarray):
        self.length = cv.arcLength(contour, True)
        self.polygon = cv.approxPolyDP(contour, 0.05 * self.length, True).reshape(-1, 2)
        self.area = cv.contourArea(self.polygon)

    def area_in_range(self, min_area: float, max_area: float) -> bool:
        return min_area < self.area < max_area

    def is_square(self, max_cos: float, max_len_ratio: float) -> bool:
        if len(self.polygon) == 4 and cv.isContourConvex(self.polygon):
            c, c1, c2 = self.polygon, np.roll(self.polygon, 1, axis=0), np.roll(self.polygon, 2, axis=0)

            lengths = [np.sqrt((c[i][0] - c1[i][0]) ** 2 + (c[i][1] - c1[i][1]) ** 2) for i in range(4)]
            cos_angles = [self.angle_cos(c[i], c1[i], c2[i]) for i in range(4)]

            if max(cos_angles) < max_cos and max(lengths) / min(lengths) < max_len_ratio:
                return True

        return False

    @staticmethod
    def angle_cos(p0, p1, p2) -> float:
        d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
        return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


class Square:
    def __init__(self, contour: np.ndarray, color=None):
        self.color = color
        self.symbol = None
        self.color_name = None

        rect = cv.minAreaRect(contour)
        self.corners = cv.boxPoints(rect).astype(int)

        (x, y), (w, h), angle = rect

        self.x = int(x)
        self.y = int(y)
        self.area = w * h
        self.angle = -angle
        self.width = int(w)
        self.height = int(h)

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


class CubePosition:
    def __init__(self, x: float, y: float, angle: float):
        self.x = x
        self.y = y
        self.angle = angle

    def cube_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 50, self.angle + r*90, 90, 0]

    def release_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 50, self.angle + r*90, 90, 0]

    def operational_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 100, self.angle + r*90, 90, 0]

    def transport_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 150, self.angle + r*90, 90, 0]
    
    def chill_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 300, self.angle + r*90, 90, 0]

    def off_screen_position(self):
        return [400, 250, 300, 0, 90, 0]