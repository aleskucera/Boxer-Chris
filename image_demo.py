import cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from src import detect_squares

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


def corners_demo(img: str):
    import numpy as np
    import cv2 as cv
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # # gray = np.float32(gray)
    # edges = cv2.Canny(gray, 50, 120)
    # dst = cv.cornerHarris(edges, 2, 5, 0.1)
    # # result is dilated for marking the corners, not important
    # dst = cv.dilate(dst, None)
    # # Threshold for an optimal value, it may vary depending on the image.
    # img[dst > 0.1 * dst.max()] = [0, 0, 255]
    #
    # # plot the results
    # images = [img[..., ::-1], edges, dst]
    # titles = ['Original image', 'Edges', 'Corners']
    #
    # for i, img in enumerate(images):
    #     plt.subplot(2, 2, i + 1)
    #     plt.imshow(img)
    #     plt.xticks([]), plt.yticks([])
    #     plt.title(titles[i])
    #
    # plt.show()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 120)
    corners = cv.goodFeaturesToTrack(gray, 1000, 0.001, 8)
    corners = np.int0(corners)

    squares_img = img.copy()
    # find squares with ransac and draw them
    for i in range(100000):
        indices = np.random.choice(corners.shape[0], 3, replace=False)
        rand_corners = corners[indices]
        rand_corners = np.squeeze(rand_corners)
        rand_corners = np.float32(rand_corners)
        square = cv.minAreaRect(rand_corners)
        box = cv.boxPoints(square)
        box = np.int0(box)

        if square[1][0] > 0.8 * square[1][1] and square[1][0] < 1.2 * square[1][1]:
            if square[1][0] > 30 and square[1][0] < 100 and square[1][1] > 30 and square[1][1] < 100:
                cv.drawContours(squares_img, [box], 0, (0, 0, 255), 2)

    corners_img = img.copy()
    for i in corners:
        x, y = i.ravel()
        cv.circle(corners_img, (x, y), 2, 255, -1)

    # plot the results
    images = [img[..., ::-1], edges, corners_img[..., ::-1], squares_img[..., ::-1]]
    titles = ['Original image', 'Edges', 'Corners', 'Squares']

    for i, img in enumerate(images):
        plt.subplot(2, 2, i + 1)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])

    plt.show()


if __name__ == '__main__':
    image = cv2.imread('edges/edges_chaos_in0.png')
    squares_demo(image, 'orange', 'conf/main.yaml')
    corners_demo(image)

    plt.imshow(image)
    plt.show()
