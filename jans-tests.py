import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('TkAgg')


if __name__ == '__main__':

    img = cv2.imread('edges/edges_chaos_in5.png')

    plt.subplot(2, 2, 1)
    plt.imshow(img)
    plt.xticks([]), plt.yticks([])
    plt.title("Original image")

