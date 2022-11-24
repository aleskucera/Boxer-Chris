import cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from src import detect_squares, colors_at_edges

matplotlib.use('TkAgg')


def squares_demo(image: np.ndarray, color: str, config_file: str) -> None:
    # Process image
    edges, image_f1, image_f2, thresh, contours, squares = detect_squares(image, color, config_file)

    if color in ['orange', 'yellow']:
        plt_color = (112, 25, 25)
    else:
        plt_color = (175, 0, 255)

    # Plot the results
    result = np.full(image.shape, 255)
    result = cv2.bitwise_and(result, result, mask=edges)
    for square in squares:
        cv2.circle(result, (int(square.x), int(square.y)), 8, (175, 0, 255), -1)
        for i in range(4):
            cv2.circle(result, (int(square.corners[i, 0]), int(square.corners[i, 1])), 8, (175, 0, 255), -1)

        print(f'width: {square.width}, height: {square.height}, area: {square.area}')

    # Draw the contours
    contours_image = image.copy()
    cv2.drawContours(contours_image, contours, -1, plt_color, 4)

    images = [image[..., ::-1], image_f1[..., ::-1], image_f2[..., ::-1],
              thresh, contours_image[..., ::-1], result[..., ::-1]]
    titles = ['Original image', 'Processed image', 'Color Filter', 'Threshold', 'Contours', f'Detected {color} squares']

    for i, img in enumerate(images):
        plt.subplot(2, 3, i + 1)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])

    plt.show()


if __name__ == '__main__':
    image = cv2.imread('imgs_for_our_dear_Ales/5.png')
    squares_demo(image, 'blue', 'conf/main.yaml')
    edge_colors = colors_at_edges(image, 100, 'conf/main.yaml')
    print(edge_colors)