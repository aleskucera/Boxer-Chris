import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

# read image
img = plt.imread('colors/orange.png')
# img = plt.imread('imgs_for_our_dear_Ales/02input_color_image.png')
print(np.max(img))
print(np.min(img))


# plot every 10th point to 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

k = 5

ax.scatter(img[::k, ::k, 0].flatten(), img[::k, ::k, 1].flatten(), img[::k, ::k, 2].flatten(), c=img[::k, ::k, :]
           .flatten().reshape(-1, 3), marker='o', s=5)

ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')
# change axis limits
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_zlim([0, 1])
plt.show()