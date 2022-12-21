import cv2 as cv


def visualize_squares(image, squares, mode='centers'):
    for square in squares:
        cv.drawContours(image, [square.corners], 0, square.vis_color[::-1], 2)

        if mode == 'centers':
            cv.putText(image, f'{square.x, square.y}', (square.x - 30, square.y + 10),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, square.vis_color[::-1], 1)
        elif mode == 'areas':
            cv.putText(image, f'{int(square.area)}', (square.x - 20, square.y + 10),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, square.vis_color[::-1], 1)
        elif mode == 'ids':
            cv.putText(image, f'{square.id}', (square.x - 10, square.y + 10),
                       cv.FONT_HERSHEY_SIMPLEX, 1, square.vis_color[::-1], 2)
        elif mode == 'angles':
            cv.putText(image, f'{square.angle}', (square.x - 10, square.y + 10),
                       cv.FONT_HERSHEY_SIMPLEX, 1, square.vis_color[::-1], 2)
        else:
            raise ValueError('Unknown visualization mode: {}'.format(mode))

    cv.imshow('image', image)
    cv.waitKey(0)
    cv.destroyAllWindows()
