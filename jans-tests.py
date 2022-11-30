import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt
from src import map_color

matplotlib.use('TkAgg')


class SquareImg:
    def __init__(self, img: np.ndarray, center, dimensions):
        self.img = img
        self.center = center
        self.dimensions = dimensions


def fit_square(img: np.ndarray) -> np.ndarray:
    # detect edges
    edges = cv2.Canny(img, 50, 100)

    # find non-zero pixels (indices of edge pixels)
    idx_nonzero = np.argwhere(edges)

    # TODO: delete this part
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, minLineLength=30, maxLineGap=30)
    if lines is None:
        return img

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(edges, (x1, y1), (x2, y2), (100, 100, 100), 2)
        cv2.imshow("lines", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # plot edges
    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    return img


def fit_square_ransac(img: np.ndarray, iterations=1000) -> np.ndarray:

    return img


def convert_to_black_and_white(img: np.ndarray) -> np.ndarray:
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(grey, 254, 255, cv2.THRESH_BINARY)
    return bw


def get_square_imgs(img: np.ndarray) -> np.ndarray:
    edges = cv2.Canny(img, 100, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    sqr_imgs = []
    for i, contour in enumerate(contours):
        x,y,w,h = cv2.boundingRect(contour)
        cropped_contour = img[y:y+h, x:x+w]

        sqr_img = SquareImg(cropped_contour, (x, y), (w, h))
        sqr_imgs.append(sqr_img)

        # cv2.imshow(f"contour {i}", cropped_contour)
        # cv2.waitKey(0)

    cv2.destroyAllWindows()
    return np.array(sqr_imgs, dtype=SquareImg)


def get_corners(img: np.ndarray) -> np.ndarray:
    # convert image to gray scale image
    # bw = convert_to_black_and_white(img)
    bw = img
    # contours
    cnt, _ = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnt:
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        cv2.drawContours(img, approx, -1, (255, 0, 0), 10)

    cv2.imshow("contours", img)
    return img


if __name__ == '__main__':

    orig = cv2.imread('edges/edges_chaos5.png')

    img = cv2.imread('images/label.png')

    img = map_color(img, 'conf/main.yaml')

    # print unique colors
    unique, counts = np.unique(img.reshape(-1, img.shape[2]), axis=0, return_counts=True)
    print(unique)

    # corners = get_corners(img)

    objects = get_square_imgs(convert_to_black_and_white(img))
    for object in objects:
        get_corners(object.img)
        # fit_square(object.img)
        fit_square_ransac(object.img)

    plt.subplot(2, 2, 1)
    plt.imshow(orig[..., ::-1])
    plt.xticks([]), plt.yticks([])
    plt.title("Original image")

    plt.subplot(2, 2, 2)
    plt.imshow(img)
    plt.xticks([]), plt.yticks([])
    plt.title("Labeled image")

    plt.subplot(2, 2, 3)
    plt.imshow(convert_to_black_and_white(img))
    plt.xticks([]), plt.yticks([])
    plt.title(f"Only color")

    plt.show()
