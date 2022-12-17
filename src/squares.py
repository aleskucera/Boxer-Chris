import cv2 as cv
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


class Contour:
    def __init__(self, contour):
        self.contour = contour
        self.area = cv.contourArea(contour)

    def area_in_range(self, min_area=1000, max_area=100000):
        return min_area < self.area < max_area

    def is_square(self, max_cos=0.04, max_len_ratio=1.08):
        if len(self.contour) == 4 and cv.isContourConvex(self.contour):
            lengths = [np.sqrt((self.contour[i][0] - self.contour[(i + 1) % 4][0]) ** 2 +
                               (self.contour[i][1] - self.contour[(i + 1) % 4][1]) ** 2) for i in range(4)]
            cos_angles = [self.angle_cos(self.contour[i], self.contour[(i + 1) % 4], self.contour[(i + 2) % 4])
                          for i in range(4)]
            if max(cos_angles) < max_cos and max(lengths) / min(lengths) < max_len_ratio:
                return True
        return False
    @staticmethod
    def angle_cos(p0, p1, p2):
        d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
        return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))

class Square:
    def __init__(self, contour, color):
        self.color = color
        self.corners = contour

        self.center = np.mean(contour, axis=0)
        self.area = cv.contourArea(contour)

    def is_inside(self, point: tuple):
        return cv.pointPolygonTest(self.corners, point, False) >= 0

    def __lt__(self, other):
        return self.area < other.area

    def __gt__(self, other):
        return self.area > other.area

    def __eq__(self, other):
        return self.area == other.area

    def __ne__(self, other):
        return self.area != other.area

def find_squares2(img):
    vectors = []
    squares = []
    for img in glob('../camera/images8/*.png'):
        img = cv.imread(img)
        img = cv.GaussianBlur(img, (5, 5), 0)

        # find squares in every color plane of the image
        for gray, color in zip(cv.split(img), ['b', 'g', 'r']):

            # try several threshold levels
            for thresh in range(10, 220, 1):

                # Threshold the image
                _retval, bin = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY)

                # Find contours and store them in a list
                contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

                # Test contours
                for cnt in contours:
                    cnt = Contour(cnt)
                    if cnt.area_in_range() and cnt.is_square():
                        vectors.append(cnt.contour.reshape(1, 8))
                        squares.append(cnt.contour)

    vectors = np.array(vectors)
    squares = np.array(squares)
    clustering = DBSCAN(eps=20, min_samples=2).fit(vectors)

    final_squares = []
    final_centers = []
    final_areas = []
    ret = []
    # Calculate the mean of each cluster
    for i in range(np.max(clustering.labels_) + 1):
        mean = np.mean(squares[clustering.labels_ == i], axis=0, dtype=np.int32)
        final_squares.append(mean)
        final_centers.append(np.mean(mean, axis=0))
        final_areas.append(cv.contourArea(mean))

        ret.append(Square(mean, [0, 0, 0]))
    return ret

def is_square(cnt, min_area=1000, max_area=100000, max_cos=0.02, max_len_ratio=1.04):
    """Test if the contour is a square"""

    # Test if the contour has 4 vertices and is convex
    if len(cnt) == 4 and cv.isContourConvex(cnt):

        # Filter contours by area
        if cv.contourArea(cnt) > min_area and cv.contourArea(cnt) < max_area:
            cnt = cnt.reshape(-1, 2)

            # calculate length of each side
            lengths = [np.sqrt((cnt[i][0] - cnt[(i + 1) % 4][0]) ** 2 + (cnt[i][1] - cnt[(i + 1) % 4][1]) ** 2)
                       for i in range(4)]

            # calculate angle of each side and take the maximum
            cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])

            # Filter contours by length and angle
            if cos < max_cos and max(lengths) / min(lengths) < max_len_ratio:
                return True
    return False


def find_squares(img):
    squares = []
    img = cv.GaussianBlur(img, (5, 5), 0)

    # find squares in every color plane of the image
    for gray, color in zip(cv.split(img), ['b', 'g', 'r']):

        # try several threshold levels
        for thresh in range(10, 220, 1):

            # Threshold the image
            _retval, bin = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY)

            # Find contours and store them in a list
            contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            # Test contours
            for cnt in contours:

                # Approximate the contour with accuracy proportional to the contour perimeter
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02 * cnt_len, True)

                # Test if the contour is a square
                cnt = cnt.reshape(-1, 2)
                if is_square(cnt):
                    squares.append(cnt)

    squares = np.array(squares)
    return squares

def main():
    square_list = []
    for img in glob('../camera/images8/*.png'):
        img = cv.imread(img)
        squares = find_squares2(img)
        square_list.append(squares)

    # Merge all squares
    squares = np.concatenate(square_list, axis=0)
    square_vectors = squares.reshape(squares.shape[0], -1)

    clustering = DBSCAN(eps=20, min_samples=2).fit(square_vectors)

    # map labels to colors
    cm = plt.get_cmap('gist_rainbow')
    colors = [cm(1. * i / (np.max(clustering.labels_) + 1)) for i in range(np.max(clustering.labels_) + 1)]
    colors = np.array(colors)
    colors = np.vstack([colors, (0, 0, 0, 1)])

    final_squares = []
    final_centers = []
    final_areas = []
    # Calculate the mean of each cluster
    for i in range(np.max(clustering.labels_) + 1):
        mean = np.mean(squares[clustering.labels_ == i], axis=0, dtype=np.int32)
        final_squares.append(mean)
        final_centers.append(np.mean(mean, axis=0))
        final_areas.append(cv.contourArea(mean))


    num_squares = len(final_squares)
    for i in range(num_squares):
        if final_squares[i] is not None:
            for j in range(i + 1, num_squares):
                if final_squares[j] is not None:
                    if i != j and cv.pointPolygonTest(final_squares[j], tuple(final_centers[i]), False) >= 0:
                        if final_areas[i] > final_areas[j]:
                            final_squares[i] = None
                        else:
                            final_squares[j] = None

    final_squares = [x for x in final_squares if x is not None]



    for i in range(len(final_squares)):
        color = colors[i]
        cv.drawContours(img, [final_squares[i]], -1, [int(255 * x) for x in color], 3)


    # Save the image
    cv.imwrite('output.png', img)

    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()