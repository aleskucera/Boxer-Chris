import os
import itertools
from copy import deepcopy

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
    # Find contours
    dark_contours, dark_image, light_contours, light_image = find_contours(directory, MIN_THRESHOLD, MAX_THRESHOLD, STEP)

    # Visualize contours
    # cv.drawContours(dark_image, dark_contours, -1, (0, 255, 0), 3)
    # cv.imshow('image', dark_image)
    # cv.waitKey(0)

    # Create Square objects
    dark_squares = squares_from_contours(dark_contours, dark_image, mode='min')
    light_squares = squares_from_contours(light_contours, light_image, mode='mean')

    # Find color of each square
    dark_squares = assign_attributes(dark_squares, dark_image, config, 'dark')
    light_squares = assign_attributes(light_squares, light_image, config, 'light')

    return dark_squares + light_squares


def squares_from_contours(contours_list: list, image,mode: str = 'min') -> list:
    squares = []
    labels, vectors = cluster_square_contours(contours_list)
    contours = vectors.reshape(-1, 4, 1, 2)

    # Visualize the contours
    # cv.drawContours(image, contours, -1, (0, 255, 0), 3)
    # cv.imshow('image', image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # Create Square objects
    for i in range(np.max(labels) + 1):
        tmp = contours[labels == i]
        min_idx = np.argmin([cv.contourArea(c) for c in tmp])
        max_idx = np.argmax([cv.contourArea(c) for c in tmp])
        mean = np.mean(contours[labels == i], axis=0, dtype=np.int32)
        if mode == 'min':
            squares.append(Square(tmp[min_idx]))
        elif mode == 'max':
            squares.append(Square(tmp[max_idx]))
        elif mode == 'mean':
            squares.append(Square(mean))
        else:
            raise ValueError('Invalid mode')

    for s1, s2 in itertools.combinations(squares, 2):
        if s1.is_inside((s2.x, s2.y)) or s2.is_inside((s1.x, s1.y)):
            if s1 > s2:
                s1.outer_square = True
            else:
                s2.outer_square = True

    return [square for square in squares if not square.outer_square]


def find_contours(directory: str, lower: int, upper: int, step: int):
    """Finds contours in the given images
    :param directory: directory containing images of the cubes
    :param lower: Lower threshold
    :param upper: Upper threshold
    :param step: Step size for threshold
    """
    dark_contours, light_contours = [], []
    dark_image, light_image = None, None
    for file in os.scandir(directory):
        file_path = os.path.join(directory, file.name)
        img = cv.imread(file_path)

        if 'dark' in file.name:
            dark_image = deepcopy(img)
            img = correction(img, 0.2, 0.2, 3, 0.2, 0.2, 3, 0.6)
            img = cv.bilateralFilter(img, 30, 5, 5)
            img = cv.bilateralFilter(img, 30, 10, 10)
            img = cv.bilateralFilter(img, 30, 20, 20)
            img = cv.bilateralFilter(img, 30, 30, 30)
            img = cv.bilateralFilter(img, 20, 40, 40)

            # Visualize the image
            cv.imshow('image', img)
            cv.waitKey(0)
            cv.destroyAllWindows()

            for channel in cv.split(img):
                for threshold in range(lower, upper, step):
                    _, thresh = cv.threshold(channel, threshold, 255, cv.THRESH_BINARY)
                    contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
                    dark_contours.extend(contours)

        elif 'light' in file.name:
            light_image = deepcopy(img)
            img = correction(img, 0.3, 0.3, 7, 0.1, 0.1, 3, 0.6)
            img = cv.bilateralFilter(img, 10, 5, 5)
            img = cv.bilateralFilter(img, 20, 10, 10)
            img = cv.bilateralFilter(img, 20, 20, 20)

            # Visualize the image
            # cv.imshow('image', img)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

            for channel in cv.split(img):
                for threshold in range(lower, upper, step):
                    _, thresh = cv.threshold(channel, threshold, 255, cv.THRESH_BINARY)
                    contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
                    light_contours.extend(contours)

        else:
            continue

    return dark_contours, dark_image, light_contours, light_image


def cluster_square_contours(contours: list, eps: int = DB_EPSILON, min_samples: int = DB_MIN_SAMPLES) -> tuple:
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


def assign_attributes(squares: list, image: np.ndarray, config: dict, shade: str) -> list:
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    filtered_squares = []

    for square in squares:
        pixels = []

        for color in config['colors'].values():
            mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)


            cv.drawContours(mask, [square.corners], -1, 255, -1)
            square_hsv = cv.bitwise_and(hsv_image, hsv_image, mask=mask)

            # Visualize the mask
            cv.imshow('mask', square_hsv)
            cv.waitKey(0)
            cv.destroyAllWindows()

            lower = np.array(color['lower'])
            upper = np.array(color['upper'])

            filtered_image = cv.inRange(square_hsv, lower, upper)
            pixels.append(np.sum(filtered_image))

            print(f'{color["color"]}: {np.sum(filtered_image)}')

            # Visualize the image
            cv.imshow('image', filtered_image)
            cv.waitKey(0)
            cv.destroyAllWindows()

        if config['colors'][np.argmax(pixels)]['shade'] == shade:
            square.vis_color = config['colors'][np.argmax(pixels)]['rgb']
            square.symbol = config['colors'][np.argmax(pixels)]['symbol']
            square.color = config['colors'][np.argmax(pixels)]['color']

            for i, (ub, lb) in enumerate(zip(config['boundaries']['upper'], config['boundaries']['lower'])):
                if lb < square.area < ub:
                    square.id = i

            filtered_squares.append(square)
    return filtered_squares

def correction(img, shadow_amount_percent, shadow_tone_percent, shadow_radius,
               highlight_amount_percent, highlight_tone_percent, highlight_radius,
               color_percent):
    """
    Image Shadow / Highlight Correction. The same function as it in Photoshop / GIMP
    :param img: input RGB image numpy array of shape (height, width, 3)
    :param shadow_amount_percent [0.0 ~ 1.0]: Controls (separately for the highlight and shadow values in the image) how much of a correction to make.
    :param shadow_tone_percent [0.0 ~ 1.0]: Controls the range of tones in the shadows or highlights that are modified.
    :param shadow_radius [>0]: Controls the size of the local neighborhood around each pixel
    :param highlight_amount_percent [0.0 ~ 1.0]: Controls (separately for the highlight and shadow values in the image) how much of a correction to make.
    :param highlight_tone_percent [0.0 ~ 1.0]: Controls the range of tones in the shadows or highlights that are modified.
    :param highlight_radius [>0]: Controls the size of the local neighborhood around each pixel
    :param color_percent [-1.0 ~ 1.0]:
    :return:
    """
    shadow_tone = shadow_tone_percent * 255
    highlight_tone = 255 - highlight_tone_percent * 255

    shadow_gain = 1 + shadow_amount_percent * 6
    highlight_gain = 1 + highlight_amount_percent * 6

    # extract RGB channel
    height, width = img.shape[:2]
    img = img.astype(np.float)
    img_R, img_G, img_B = img[..., 2].reshape(-1), img[..., 1].reshape(-1), img[..., 0].reshape(-1)

    # The entire correction process is carried out in YUV space,
    # adjust highlights/shadows in Y space, and adjust colors in UV space
    # convert to Y channel (grey intensity) and UV channel (color)
    img_Y = .3 * img_R + .59 * img_G + .11 * img_B
    img_U = -img_R * .168736 - img_G * .331264 + img_B * .5
    img_V = img_R * .5 - img_G * .418688 - img_B * .081312

    # extract shadow / highlight
    shadow_map = 255 - img_Y * 255 / shadow_tone
    shadow_map[np.where(img_Y >= shadow_tone)] = 0
    highlight_map = 255 - (255 - img_Y) * 255 / (255 - highlight_tone)
    highlight_map[np.where(img_Y <= highlight_tone)] = 0

    # // Gaussian blur on tone map, for smoother transition
    if shadow_amount_percent * shadow_radius > 0:
        # shadow_map = cv2.GaussianBlur(shadow_map.reshape(height, width), ksize=(shadow_radius, shadow_radius), sigmaX=0).reshape(-1)
        shadow_map = cv.blur(shadow_map.reshape(height, width), ksize=(shadow_radius, shadow_radius)).reshape(-1)

    if highlight_amount_percent * highlight_radius > 0:
        # highlight_map = cv2.GaussianBlur(highlight_map.reshape(height, width), ksize=(highlight_radius, highlight_radius), sigmaX=0).reshape(-1)
        highlight_map = cv.blur(highlight_map.reshape(height, width), ksize=(highlight_radius, highlight_radius)).reshape(-1)

    # Tone LUT
    t = np.arange(256)
    LUT_shadow = (1 - np.power(1 - t * (1 / 255), shadow_gain)) * 255
    LUT_shadow = np.maximum(0, np.minimum(255, np.int_(LUT_shadow + .5)))
    LUT_highlight = np.power(t * (1 / 255), highlight_gain) * 255
    LUT_highlight = np.maximum(0, np.minimum(255, np.int_(LUT_highlight + .5)))

    # adjust tone
    shadow_map = shadow_map * (1 / 255)
    highlight_map = highlight_map * (1 / 255)

    iH = (1 - shadow_map) * img_Y + shadow_map * LUT_shadow[np.int_(img_Y)]
    iH = (1 - highlight_map) * iH + highlight_map * LUT_highlight[np.int_(iH)]
    img_Y = iH

    # adjust color
    if color_percent != 0:
        # color LUT
        if color_percent > 0:
            LUT = (1 - np.sqrt(np.arange(32768)) * (1 / 128)) * color_percent + 1
        else:
            LUT = np.sqrt(np.arange(32768)) * (1 / 128) * color_percent + 1

        # adjust color saturation adaptively according to highlights/shadows
        color_gain = LUT[np.int_(img_U ** 2 + img_V ** 2 + .5)]
        w = 1 - np.minimum(2 - (shadow_map + highlight_map), 1)
        img_U = w * img_U + (1 - w) * img_U * color_gain
        img_V = w * img_V + (1 - w) * img_V * color_gain

    # re convert to RGB channel
    output_R = np.int_(img_Y + 1.402 * img_V + .5)
    output_G = np.int_(img_Y - .34414 * img_U - .71414 * img_V + .5)
    output_B = np.int_(img_Y + 1.772 * img_U + .5)

    output = np.row_stack([output_B, output_G, output_R]).T.reshape(height, width, 3)
    output = np.minimum(output, 255).astype(np.uint8)
    return output
