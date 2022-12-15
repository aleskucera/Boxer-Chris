import cv2
import cv2.aruco as aruco
import numpy as np


# Calibrate camera based on the ChArUco image
def calibrate_charuco(image, charuco_dict, board):
    # Detect ChArUco corners
    corner_list = []
    id_list = []

    aruco_params = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(image, charuco_dict, parameters=aruco_params)
    resp, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, image, board)

    if resp > 10:
        corner_list.append(charuco_corners)
        id_list.append(charuco_ids)

    # Calibrate camera
    image_size = image.shape[:2]
    retval, camera_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(corner_list, id_list,
                                                                                    board, image_size, None, None)

    return retval, camera_matrix, dist_coeffs, rvecs, tvecs



# Draw the detected ChArUco board
def draw_charuco_board(image, charuco_dict, board):
    # Detect ChArUco corners
    corners, ids, rejected = aruco.detectMarkers(image, charuco_dict)
    charuco_res = aruco.interpolateCornersCharuco(corners, ids, image, board)
    image = aruco.drawDetectedMarkers(image, corners, ids)

    if charuco_res[1] is not None and charuco_res[2] is not None and len(charuco_res[1]) > 3:
        image = aruco.drawDetectedCornersCharuco(image, charuco_res[1], charuco_res[2])
    return image


def main():
    # Load the ChArUco board
    charuco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    board = aruco.CharucoBoard_create(6, 6, 0.025, 0.019, charuco_dict)

    # Load the image
    image = cv2.imread('charuco/image_4.jpg')
    # Calibrate camera
    retval, camera_matrix, dist_coeffs, rvecs, tvecs = calibrate_charuco(image, charuco_dict, board)
    # Draw the detected ChArUco board
    image = draw_charuco_board(image, charuco_dict, board)

    # Save the result
    cv2.imwrite('charuco/result_4.jpg', image)


if __name__ == '__main__':
    main()