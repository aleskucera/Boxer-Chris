import numpy as np
from copy import copy

from .objects import Cube
from .robCRSgripper import robCRSgripper
from .interpolation import interpolate_poly, interpolate_p_spline, interpolate_b_spline


def move_cube(commander, c0: Cube, c1: Cube, off_screen_pos: list, center_dest: bool = True):
    """ Moves the cube from c0 to c1. """
    # Center cubes
    if center_dest:
        c1 = center_cube(commander, c1, release=True)
    c0 = center_cube(commander, c0)

    # Move to the destination
    move(commander, c0.cube_level, c0.transport_level)
    move(commander, c0.transport_level, c1.transport_level)

    if center_dest:
        move(commander, c1.transport_level, c1.pre_release_level)
        move(commander, c1.pre_release_level, c1.release_level, step=1)

        robCRSgripper(commander, -1)
        commander.wait_gripper_ready()
        
        move(commander, c1.release_level, c1.post_release_cube_level)

        robCRSgripper(commander, c1.grip_power)
        commander.wait_gripper_ready()

        move(commander, c1.post_release_cube_level, c1.cube_level)

    else:
        move(commander, c1.transport_level, c1.cube_level)

    # Release the cube
    robCRSgripper(commander, -1)
    commander.wait_gripper_ready()
    
    # Move to the off-screen position
    move(commander, c1.operational_level, off_screen_pos, step=6)


def center_cube(commander, c: Cube, release: bool = False):
    """ Centers the cube in the gripper and sets the cube angle to 0°. """

    # Move to the cube
    move(commander, c.transport_level_rot, c.cube_level_rot)

    # Grip the cube and rotate it to 0 degrees
    robCRSgripper(commander, c.grip_power)
    commander.wait_gripper_ready()

    current_position = copy(c.cube_level_rot)
    c.angle = 0

    move(commander, current_position, c.cube_level_rot)

    robCRSgripper(commander, -1)
    commander.wait_gripper_ready()

    # Rotate the gripper
    move(commander, c.cube_level_rot, c.operational_level_rot)
    move(commander, c.operational_level_rot, c.operational_level)
    move(commander, c.operational_level, c.cube_level)

    robCRSgripper(commander, c.grip_power)
    commander.wait_gripper_ready()
    
    if release:
        robCRSgripper(commander, -1)
        commander.wait_gripper_ready()

        # Move to the operational position
        move(commander, c.cube_level, c.operational_level)

    return c


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
    x0 = np.array(x0, dtype=object)
    x1 = np.array(x1, dtype=object)
    rng = int(np.linalg.norm(x0 - x1) / step)
    try:
        normal = (x1 - x0) / np.linalg.norm(x0 - x1)
    except Exception:
        return None
    x = x0
    sol = [commander.find_closest_ikt(x)]
    for _ in range(rng):
        x = x + normal * step
        prev_x = commander.find_closest_ikt(x, sol[-1])
        sol.append(prev_x)

    sol.append(commander.find_closest_ikt(x1, sol[-1]))
    sol = np.array(sol)

    try:
        move_spline(sol, commander, 'b-spline', 2)
        return
    except Exception:
        print('Not enough points for b-spline order 2')
    
    try:
        move_spline(sol, commander, 'poly', 2)
        return
    except Exception:
        print('Not enough points for polynomial order 1')
        return

def is_reachable(commander, c: Cube):
    try:
        commander.find_closest_ikt(c.cube_level)
        return True
    except ValueError:
        return False
