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

    def cube_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 50, self.angle + r*90, 90, 0]

    def release_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 120, self.angle + r*90, 90, 0]

    def operational_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 80, self.angle + r*90, 90, 0]

    def transport_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 150, self.angle + r*90, 90, 0]
    
    def chill_level(self, rotated: bool = False):
        r = 1 if rotated else 0
        return [self.x, self.y, 300, self.angle + r*90, 90, 0]

def move_spline(trajectory, commander, spline, order):
    spline_params = []

    if spline == 'poly':
        order = 3
        spline_params = interpolate_poly(trajectory)
    if spline == 'b-spline':
        spline_params = interpolate_b_spline(trajectory, order=order)
    if spline == 'p-spline':
        num_segments = int(len(trajectory) / 3)
        poly_deg = order
        penalty_order = 2
        lambda_ = 0.1
        spline_params = interpolate_p_spline(trajectory, num_segments, poly_deg, penalty_order, lambda_)

    commander.move_to_pos(trajectory[0])
    commander.wait_ready(sync=True)
    for i in range(len(spline_params)):
        commander.splinemv(spline_params[i], order=order)
    commander.wait_ready(sync=True)

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
    center_cube(commander, x0)
    sol = line_trajectory(commander, x0.operational_level(), x0.cube_level())
    move_spline(sol, commander, 'poly', 2)
    
    robCRSgripper(commander, GRIP)
    commander.wait_ready()

    sol = line_trajectory(commander, x0.cube_level(), x0.transport_level())
    move_spline(sol, commander, 'poly', 2)

    sol = line_trajectory(commander, x0.transport_level(), x1.transport_level())
    move_spline(sol, commander, 'poly', 2)

    sol = line_trajectory(commander, x1.transport_level(), x1.release_level())
    move_spline(sol, commander, 'poly', 2)

    robCRSgripper(commander, RELEASE)
    commander.wait_ready()
    
    sol = line_trajectory(commander, x1.release_level(), x1.operational_level())
    move_spline(sol, commander, 'poly', 2)

    p = CubePosition(400, 200, 0)
    sol = line_trajectory(commander, x1.operational_level(), p.operational_level())
    move_spline(sol, commander, 'poly', 2)

def center_cube(commander, x: CubePosition):
    sol = line_trajectory(commander, x.operational_level(), x.cube_level())
    move_spline(sol, commander, 'poly', 2)

    robCRSgripper(commander, GRIP)
    commander.wait_ready()

    robCRSgripper(commander, RELEASE)
    commander.wait_ready()

    sol = line_trajectory(commander, x.cube_level(), x.operational_level())
    move_spline(sol, commander, 'poly', 2)

    sol = line_trajectory(commander, x.operational_level(), x.operational_level(rotated=True))
    move_spline(sol, commander, 'poly', 2)

    sol = line_trajectory(commander, x.operational_level(rotated=True), x.cube_level(rotated=True))
    move_spline(sol, commander, 'poly', 2)

    robCRSgripper(commander, GRIP)
    commander.wait_ready()

    robCRSgripper(commander, RELEASE)
    commander.wait_ready()

    sol = line_trajectory(commander, x.cube_level(rotated=True), x.operational_level(rotated=True))
    move_spline(sol, commander, 'poly', 2)



def main():
    robot = robCRS97()
    tty_dev = '/dev/ttyUSB0'
    commander = Commander(robot)  # initialize commander
    commander.open_comm(tty_dev, speed=19200)  # connect to control unit

    # commander.init(reg_type=None, max_speed=None, hard_home=True)
    # robCRSgripper(commander, RELEASE)
    # commander.wait_ready()

    # p0 = CubePosition(400, -200, 0)
    # p1 = CubePosition(400, 200, 0)
    p0 = CubePosition(615.6, -8.6, -14.36)
    p1 = CubePosition(386.1, -128, -82.18)

    # sol = line_trajectory(commander, p1.transport_level(), p1.chill_level())
    # move_spline(sol, commander, 'poly', 2)

    move_cube(commander, p0, p1)
    # center_cube(commander, p0)

if __name__ == "__main__":
    main()
