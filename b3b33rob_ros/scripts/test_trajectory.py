import numpy as np
from numpy import pi
from mitsubishi_arm_student_interface.mitsubishi_robots import Mitsubishi_robot

if __name__=='__main__':
    # Create interace with moveit, ROS and others
    robot = Mitsubishi_robot()

    # Set the robot relative maximal speed (decrease for debugging is recommended)
    robot.set_max_speed(0.3)

    # Prepare waypoints in the joint coordinates
    waypoints = []
    waypoints.append([pi/4,0,pi/4,0,0,0])
    waypoints.append([pi/8,0,3*pi/8,0,0,0])
    waypoints.append([0,0,pi/2,0,pi/2,0])

    # Execute trajectory that will go through all waypoints
    robot.execute_joint_trajectory(waypoints)
