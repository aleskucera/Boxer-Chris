import numpy as np

from .objects import CubePosition
from .robCRSgripper import robCRSgripper
from .interpolation import interpolate_poly, interpolate_p_spline, interpolate_b_spline

GRIP = 0.5
RELEASE = -1


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

def move(commander, x0, x1, step=3):
    rng = int(np.linalg.norm(np.array(x0) - np.array(x1)) / step)
    normal = (np.array(x1) - np.array(x0)) / np.linalg.norm(np.array(x0) - np.array(x1))
    x = x0
    sol = [commander.find_closest_ikt(x)]
    for i in range(rng):
        x = x + normal * step
        prev_x = commander.find_closest_ikt(x, sol[-1])
        sol.append(prev_x)

    sol = np.array(sol)
    move_spline(sol, commander, 'poly', 3)


def move_cube(commander, p0: CubePosition, p1: CubePosition, config: dict, center_dest: bool = True):
    p = config['base_position']
    off_screen_position = [p['x'], p['y'], p['z'], 0, p['angle'], 0]

    if center_dest:
        center_cube(commander, p1)
    center_cube(commander, p0)
    
    move(commander, p0.operational_level(), p0.cube_level())
    
    robCRSgripper(commander, GRIP)
    commander.wait_gripper_ready()

    move(commander, p0.cube_level(), p0.transport_level())
    move(commander, p0.transport_level(), p1.transport_level())
    move(commander, p1.transport_level(), p1.cube_level())

    robCRSgripper(commander, RELEASE)
    commander.wait_gripper_ready()
    
    move(commander, p1.cube_level(), p1.operational_level())
    move(commander, p1.operational_level(), off_screen_position)
    

def center_cube(commander, x: CubePosition):
    move(commander, x.operational_level(), x.cube_level())

    robCRSgripper(commander, GRIP)
    commander.wait_gripper_ready()

    robCRSgripper(commander, RELEASE)
    
    commander.wait_gripper_ready()

    move(commander, x.cube_level(), x.operational_level())
    move(commander, x.operational_level(), x.operational_level(rotated=True))
    move(commander, x.operational_level(rotated=True), x.cube_level(rotated=True))

    robCRSgripper(commander, GRIP)
    commander.wait_gripper_ready()

    robCRSgripper(commander, RELEASE)
    commander.wait_gripper_ready()

    move(commander, x.cube_level(rotated=True), x.operational_level(rotated=True))





