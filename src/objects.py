import cv2 as cv
import numpy as np


class ApproxPolygon:
    """Approximate polygon for a square detection in the image.
    The object approximates the contour of the square and calculates its area.
    Its functionality is to determine whether the contour is a square or not.
    """

    def __init__(self, contour: np.ndarray):
        self.length = cv.arcLength(contour, True)
        self.polygon = cv.approxPolyDP(contour, 0.03 * self.length, True).reshape(-1, 2)
        self.area = cv.contourArea(self.polygon)

    def area_in_range(self, min_area: float, max_area: float) -> bool:
        return min_area < self.area < max_area

    def is_square(self, max_cos: float, max_len_ratio: float) -> bool:
        """Check if the polygon is a square
        :param max_cos: maximum cosine of the angle between the sides of the polygon
        :param max_len_ratio: maximum ratio between the length of the sides of the polygon
        """
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
    """Object representing a detected square in the image.
    The object contains information about the square's position, color, and ID (size information).
    It can be used to create a Cube object or for visualization.
    """

    def __init__(self, contour: np.ndarray, vis_color=None):
        self.id = None
        self.color = None
        self.symbol = None
        self.vis_color = vis_color

        rect = cv.minAreaRect(contour)
        self.corners = cv.boxPoints(rect).astype(int)

        (x, y), (w, h), angle = rect

        self.x = int(x)
        self.y = int(y)
        self.area = cv.contourArea(contour)
        self.angle = -angle
        self.width = int(w)
        self.height = int(h)

        self.outer_square = None
        self.parent_id = None

    def is_inside(self, point: tuple):
        point = tuple(map(float, point))
        return cv.pointPolygonTest(self.corners, point, False) > 0

    def create_cube(self, A: np.ndarray, b: np.ndarray, motion_config: dict):
        camera_coords = np.array([[self.x], [self.y]])
        global_coords = A @ camera_coords + b
        return Cube(global_coords[0], global_coords[1], self.angle, self.id, self.parent_id, motion_config, self.color)

    def __lt__(self, other):
        return self.area < other.area

    def __gt__(self, other):
        return self.area > other.area

    def __eq__(self, other):
        return self.area == other.area

    def __ne__(self, other):
        return self.area != other.area

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = f' SQUARE {self.id}: {self.color}\n\
                \tCenter: {(self.x, self.y)}\n\
                \tArea: {self.area}\n\
                \tAngle: {self.angle}\n\
                \tWidth and height: {(self.width, self.height)}\n\
                \tParent id: {self.parent_id}\n\n'
        return out


class Cube:
    """Object representing a cube in the global coordinate system.
    The object contains information about the cube's position, color, and ID (size information).
    The object is generated from a Square object. Its attributes are used for a motion planning.
    """

    def __init__(self, x: int, y: int, angle: int, size_id: int, parent_id: int, config: dict, color: str = None):
        self.x = x
        self.y = y
        self.id = size_id
        self.angle = angle
        self.color = color
        self.config = config
        self.grip_power = self.config['grip_power']
        self.parent_id = parent_id

    @property
    def cube_level(self) -> tuple:
        z = self.config['cube_level']
        return self.x, self.y, z, self.angle, 90, 0

    @property
    def cube_level_rot(self) -> tuple:
        z = self.config['cube_level']
        return self.x, self.y, z, self.angle + 90, 90, 0

    @property
    def operational_level(self) -> tuple:
        z = self.config['operational_level']
        return self.x, self.y, z, self.angle, 90, 0

    @property
    def operational_level_rot(self) -> tuple:
        z = self.config['operational_level']
        return self.x, self.y, z, self.angle + 90, 90, 0

    @property
    def transport_level(self) -> tuple:
        z = self.config['transport_level']
        return self.x, self.y, z, self.angle, 90, 0

    @property
    def transport_level_rot(self) -> tuple:
        z = self.config['transport_level']
        return self.x, self.y, z, self.angle + 90, 90, 0

    @property
    def pre_release_level(self) -> tuple:
        z = self.config['release_level'][self.parent_id]
        angle_offset = self.config['pre_release_angle_offset']
        return self.x, self.y, z, self.angle, 90 + angle_offset, 0

    @property
    def release_level(self) -> tuple:
        z = self.config['release_level'][self.parent_id]
        angle_offset = self.config['release_angle_offset']
        x_offset = self.config['release_x_offset']
        return self.x + x_offset, self.y, z, self.angle, 90 + angle_offset, 0

    @property
    def post_release_cube_level(self) -> tuple:
        z = self.config['cube_level']
        x_offset = self.config['release_x_offset']
        return self.x + x_offset, self.y, z, self.angle, 90, 0

    def is_reachable(self, commander) -> bool:
        try:
            commander.find_closest_ikt(self.cube_level)
            commander.find_closest_ikt(self.cube_level_rot)
            commander.find_closest_ikt(self.transport_level)
            commander.find_closest_ikt(self.transport_level_rot)
            return True
        except ValueError:
            print('Not reachable cube: ')
            print(f'{self.__str__}')
            return False

    def is_identified(self):
        if self.id is None or self.color is None:
            return False
        return True

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return self.id == other.id and self.color == other.color

    def __ne__(self, other):
        return self.id != other.id

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = f' CUBE {self.id}: {self.color}\n\
                \tCenter: {(self.x, self.y)}\n\
                \tAngle: {self.angle}\n\n \
                \tParent id: {self.parent_id}\n\n'
        return out
