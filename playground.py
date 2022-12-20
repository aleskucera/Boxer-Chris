import numpy as np

arr = np.array([1, 1, 2, 3, 1, 0, 1])

for u in np.unique(arr):
    print(np.where(arr == u))