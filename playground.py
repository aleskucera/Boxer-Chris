import numpy as np
from scipy.optimize import least_squares

x = np.array([[646, 523], [172, 529], [333, 525], [494, 522]])
y = np.array([87, 83.5, 83.5, 81.5])
s = np.array([[640], [480]])

def optimized_func(a, x, y, s):
    d = np.linalg.norm(s - x.T, axis=0)
    return a[0]*a[0]*d + a[1]*d + a[2] - y

x0 = [1, 1, 1]
x = least_squares(optimized_func, x0, args=(x, y, s)).x
print(x)