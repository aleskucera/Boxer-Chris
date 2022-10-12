
# main rospy package
import rospy

# import pi as ros uses radians
from numpy import pi

# import the robot interface
from mitsubishi_arm_student_interface.mitsubishi_robots import Mitsubishi_robot


if __name__=='__main__':

    # Initialize robot interface class
    robot = Mitsubishi_robot()

    # Get and print current position of the robot in joint coordinates
    j = robot.get_joint_values()
    print 'Joint position:'
    print j

    # Get and print current position of the end effector in the cartesian coordinates
    c = robot.get_position()
    print 'Cartesian position:'
    print c

