import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

import cv2
from src import detect_squares


def main():
    colors = ['black', 'green', 'blue', 'red', 'orange', 'yellow']

    for color in colors:
        img = cv2.imread(f'camera/images0/{color}.png')

        print(f'Processing {color}...')

        fig = plt.figure(figsize=(16, 9))
        ax = fig.add_subplot(111, projection='3d')

        k = 5
        normalized_img = img / 255
        red = normalized_img[::k, ::k, 0].flatten()
        green = normalized_img[::k, ::k, 1].flatten()
        blue = normalized_img[::k, ::k, 2].flatten()

        ax.scatter(red, green, blue, c=normalized_img[::k, ::k, :].flatten().reshape(-1, 3), marker='o', s=5)

        ax.set_xlabel('Red')
        ax.set_ylabel('Green')
        ax.set_zlabel('Blue')
        # change axis limits
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])
        plt.show()

        # detect color squares
        edges, image_f1, image_f2, thresh, contours, squares = detect_squares(img, color, 'conf/main.yaml')

        # edges to rgb
        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB).copy()
        # apply mask
        result = cv2.bitwise_and(img, result, mask=edges)
        for square in squares:
            # Draw center of the square
            result = cv2.circle(result, square.center, 10, (0, 0, 255), -1)
            # result = cv2.drawContours(result, [square.contour], -1, (0, 0, 255), 3)
            # Draw corners of the square
            for corner in square.corners:
                result = cv2.circle(result, corner, 10, (0, 255, 0), -1)

        # Plot the result
        images = [img[..., ::-1], edges, image_f1[..., ::-1], image_f2[..., ::-1], thresh, result]
        titles = ['Original', 'Edges', 'Image f1', 'Image f2', 'Thresh', 'Result']

        fig = plt.figure(figsize=(16, 9))
        for i in range(len(images)):
            ax = fig.add_subplot(2, 3, i + 1)
            ax.imshow(images[i])
            ax.set_title(titles[i])
            ax.set_xticks([])
            ax.set_yticks([])

        plt.show()


if __name__ == '__main__':
    main()
