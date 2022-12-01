"""
Simple "Square Detector" program.
Loads several images sequentially and tries to find squares in each image.
"""

import numpy as np
import cv2 as cv


def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def is_square(cnt):
    if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.contourArea(cnt) < 100000 and cv.isContourConvex(cnt):
        cnt = cnt.reshape(-1, 2)

        # calculate length of each side
        lengths = [np.sqrt((cnt[i][0] - cnt[(i + 1) % 4][0]) ** 2 + (cnt[i][1] - cnt[(i + 1) % 4][1]) ** 2)
                   for i in range(4)]
        max_len = max(lengths)
        min_len = min(lengths)

        # calculate angle of each side
        max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])

        if max_cos < 0.04 and max_len / min_len < 1.08:
            return True
    return False


def find_squares(img):
    squares = []
    img = cv.GaussianBlur(img, (5, 5), 0)

    # find squares in every color plane of the image
    for gray, color in zip(cv.split(img), ['b', 'g', 'r']):

        # try several threshold levels
        for thresh in range(5, 200, 1):

            # Threshold the image
            _retval, bin = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY)

            # save image
            # if thresh > 15 and thresh < 40:
            #     cv.imwrite(f'threshold_{thresh}_{color}.png', bin)

            # Find contours and store them in a list
            contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            # Test contours
            for cnt in contours:

                # Approximate the contour with accuracy proportional to the contour perimeter
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02 * cnt_len, True)

                # Test if the contour is a square
                if is_square(cnt):
                    squares.append(cnt)
    return squares


def main():
    from glob import glob
    for img in glob('camera/images8/*.png'):
        img = cv.imread(img)
        squares = find_squares(img)
        cv.drawContours(img, squares, -1, (0, 255, 0), 2)
        cv.imshow('squares', img)
        ch = cv.waitKey()


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
