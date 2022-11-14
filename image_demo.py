import cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from src import detect_squares, filter_edges

matplotlib.use('TkAgg')

def squares_demo(image: np.ndarray, color: str, config_file: str) -> None:
    # Detect squares
    squares, thresh, contours, filtered_image = detect_squares(image, color, config_file)

    if color in ['red', 'orange', 'yellow']:
        plt_color = (112, 25, 25)
    else:
        plt_color = (175, 0, 255)

    # Plot the results
    result = image.copy()
    for square in squares:
        cv2.drawContours(result, [square.contour], -1, plt_color, 3)
        cv2.circle(result, (int(square.x), int(square.y)), 8, plt_color, -1)
        for i in range(4):
            cv2.circle(result, (int(square.corners[i, 0]), int(square.corners[i, 1])), 8, plt_color, -1)

        print(f'width: {square.width}, height: {square.height}, area: {square.area}')

    images = [image[..., ::-1], filtered_image[..., ::-1], thresh, result[..., ::-1]]
    titles = ['Original image', 'Filtered color', 'Threshold', f'Detected {color} squares']

    for i, img in enumerate(images):
        plt.subplot(2, 2, i + 1)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])

    plt.show()

def edges_demo(image: np.ndarray, color: str, config_file: str) -> None:
    # Detect squares
    squares, thresh, contours, filtered_image = detect_squares(image, color, config_file)
    edges = filter_edges(image, 50, 150)
    result = np.full(image.shape, 255)
    result = cv2.bitwise_and(result, result, mask=edges)
    for square in squares:
        cv2.circle(result, (int(square.x), int(square.y)), 8, (175, 0, 255), -1)
        for i in range(4):
            cv2.circle(result, (int(square.corners[i, 0]), int(square.corners[i, 1])), 5, (175, 0, 255), -1)

    images = [image[..., ::-1], result[..., ::-1]]
    titles = ['Original image', f'Detected {color} squares']

    for i, img in enumerate(images):
        plt.subplot(1, 2, i + 1)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])

    plt.show()

if __name__ == '__main__':
    image = cv2.imread('imgs_for_our_dear_Ales/1.png')
    # squares_demo(image, 'orange', 'conf/main.yaml')
    edges_demo(image, 'orange', 'conf/main.yaml')

