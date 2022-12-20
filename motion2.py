import argparse
import numpy as np

from src import *

GRIP = 1
RELEASE = -1

class CubePosition:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def get_above_pos(self):
        return [self.x, self.y, 200, self.angle, 90, 0]

    def get_pos(self):
        return [self.x, self.y, 50, self.angle, 90, 0]

    def get_next_to_post(self):
        return [self.x, self.y, 50, self.angle, 0, 0]

def line_trajectory(commander, x0, x1, step=5):
    """
    Line trajectory for CRS robot.
    :param commander: Robot commander
    :param x0: starting point of trajectory
    :param x1: end point of trajectory
    :param step: step of trajectory discretisation in mm
    :return: points of trajectory
    """
    rng = int(np.linalg.norm(np.array(x0) - np.array(x1)) / step)
    normal = (np.array(x1) - np.array(x0)) / np.linalg.norm(np.array(x0) - np.array(x1))
    x = x0
    sol = [commander.find_closest_ikt(x)]
    for i in range(rng):
        x = x + normal * step
        prev_x = commander.find_closest_ikt(x, sol[-1])
        sol.append(prev_x)
    return np.array(sol)

def move_cube(commander, x0: CubePosition, x1: CubePosition):
    line_trajectory(commander, x0.get_above_pos(), x0.get_pos())
    robCRSgripper(commander, GRIP)
    line_trajectory(commander, x0.get_pos(), x0.get_above_pos())

    line_trajectory(commander, x1.get_above_pos(), x1.get_pos())
    robCRSgripper(commander, RELEASE)
    line_trajectory(commander, x1.get_pos(), x1.get_above_pos())