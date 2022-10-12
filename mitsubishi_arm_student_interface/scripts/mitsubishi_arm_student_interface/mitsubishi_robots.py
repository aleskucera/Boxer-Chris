#!/usr/bin/python

# This module was made for students of Robotics to use
# so they don't need to care about ROS nodes and stuff
# and also to force them to practice stuff from lectures,
# so something may seem odd.
# It mostly wraps moveit commander, but also adds some
# custom functions, such as trajectory given by joint
# values and calling Kinematics over KIN_6DOF object.

# About copyright, I don't care if you copy my code,
# but do so only on your own peril 

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
import numpy as np
import tf
import tf.transformations as tft
from std_msgs.msg import String
from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from moveit_commander.conversions import pose_to_list
from moveit_msgs.msg import RobotState
from sensor_msgs.msg import JointState
from moveit_msgs.msg import PlanningScene
from moveit_msgs.msg import PlanningSceneComponents
from moveit_msgs.msg import AllowedCollisionEntry
from moveit_msgs.srv import GetPlanningScene

from kinematics_6dof_ros_pkg.kinematics_6dof import KIN_6DOF
from kinematics_6dof_ros_pkg.download_from_server import download_from_server

class Mitsubishi_robot(object):
    """Move group python interface object"""

    def __init__(self):
        super(Mitsubishi_robot, self).__init__()
        
        ## Initialize `moveit_commander`_ and a `rospy`_ node:
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_python_interface', anonymous=True)
        self.listener = tf.TransformListener()
        rospy.sleep(1)

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()

        group_name = "arm"
        self.arm = moveit_commander.MoveGroupCommander(group_name)

        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

        self.kin_config = download_from_server('arm')
        # Load robot joint limits format: list of tupples (min, max)
        #self.joint_limits = []
        self.joint_limits = self.kin_config['joint_limits']
        #for i in range(1,7):
        #    maximal = float( rospy.get_param(str("/robot_description_planning/joint_limits/j"+str(i)+"/max_position")) )
        #    minimal = float( rospy.get_param(str("/robot_description_planning/joint_limits/j"+str(i)+"/min_position")) )
        #    self.joint_limits.append( (minimal,maximal) )
        
        # Load link lengths
        #self.lens = []
	#self.lens = kin_config['link_lengths']
        #for i in range(1,7):
        #    self.lens.append( float( rospy.get_param(str("/Mitsubishi_robot/len_of_link"+str(i))) ) )

        # Try load schunk gripper joint limints
        self.gripper = False
        self.gripper_cont = False
        self.eef_len = 0
        self.eef_rot = np.eye(3)
        self.eef_transform = np.eye(4)
        self.eef_trans = np.zeros((3,1))
        try:
            maximal = float( rospy.get_param(str("/robot_description_planning/joint_limits/schunk_pg70_finger_left_joint/max_position")) )
            minimal = float( rospy.get_param(str("/robot_description_planning/joint_limits/schunk_pg70_finger_left_joint/min_position")) )
            self.joint_limits.append( (minimal*2,maximal*2) )
            group_name = "hand"
            self.hand = moveit_commander.MoveGroupCommander(group_name)
            group_name = "complete"
            self.complete = moveit_commander.MoveGroupCommander(group_name)
            self.gripper = True
            self.gripper_cont = True

            #self.eef_len = float( rospy.get_param(str("/Mitsubishi_robot/len_of_gripper")) )
            #self.eef_trans[2][0] = self.eef_len
            #self.eef_transform[2][3] = self.eef_len
        except Exception as e:
            print(e)

        self.get_joint_values()
        self._max_speed = float( rospy.get_param( str("/arm/mitsubishi_arm/max_speed")))
        self._speed = 0
        self.set_max_speed(self._max_speed)
        self.kin_solver = KIN_6DOF(self.kin_config)

    def get_joint_values(self):
        """Returns complete list of current joint values in form J=[J1,J2,J3,J4,J5,J6]
           In case gripper is attached, the form is J=[J1,J2,J3,J4,J5,J6,gripper]"""
        if self.gripper:
            joints = self.arm.get_current_joint_values()
            joints += self.hand.get_current_joint_values()
        else:
            joints = self.arm.get_current_joint_values()
        return joints
    
    def set_joint_values(self, joints):
        """Sets joit values to robot
           as joints input must be a list. If list of length n<=7 (7 in case of gripper attached, 6 otherwise)
           is provided only n joints are set. If gripper is attached and joints length is 7, gripper is set too,
           else only arm joints are set.
           returns True if succeeded, else returns False"""
        joint_val = self.get_joint_values()
        
        for i in range(len(joints)):
            joint_val[i] = joints[i]
        try:
            res2 = True
            if self.gripper:
                if len(joints) == 7:
                    res = self.complete.go(joint_val[0:-1], wait=True)
                else:
                    res = self.arm.go(joint_val[0:6], wait=True)
                #res2 = self.hand.go([joint_val[6]/2]*2,wait=True)
            else:
                res = self.arm.go(joint_val, wait=True)
        except Exception as e:
            rospy.logfatal(e)
            res = False
        return res and res2
    
    def set_max_speed(self, speed):
        """Sets maximal percentage of speed to execute motion with
           maximal speed cannot be higher then maximal allowed speed
           returns True if succeeded, else returns False"""
        if speed > self._max_speed:
            rospy.logerr("Maximal allowed speed is " + str(self._max_speed))
            return False
        else:
            if self.gripper:
                self.complete.set_max_velocity_scaling_factor(speed)
                self.arm.set_max_velocity_scaling_factor(speed)
            else:
                self.arm.set_max_velocity_scaling_factor(speed)
            rospy.loginfo("Maximal speed set to " + str(speed))
            self._speed = speed
            return True
    
    def set_gripper(self, position):
        """Sets gripper open, clossed or something between.
           as position input can be used strings 'open', 'close' or float
           returns True if succeded, else returns False"""
        res = False
        if not self.gripper:
            rospy.logfatal("No gripper attached")
            return res
        if self.gripper_cont:
            if position == "open":
                res = self.hand.go([self.joint_limits[-1][1]/2]*2)
            elif position == "close":
                res = self.hand.go([self.joint_limits[-1][0]/2]*2)
            elif type(position) == float or type(position) == int :
                res = self.hand.go([float(position)/2]*2)
            return res
        else:
            return res

    def get_position(self):
        """Returns current position of end point of the robot in Cartesian coordinates as a slope vector in form P = [X,Y,Z,Rz1,Rx,Rz2]"""
        wpose = self.arm.get_current_pose().pose
        x = [wpose.position.x,
             wpose.position.y,   
             wpose.position.z]
        q = [wpose.orientation.x,
             wpose.orientation.y,   
             wpose.orientation.z,   
             wpose.orientation.w]
        e = tft.euler_from_quaternion(q,axes='szxz')
        return np.array([[x[0]],[x[1]],[x[2]],[e[2]],[e[1]],[e[0]]])

    def execute_cart_trajectory(self, waypoints):
        """Executes trajectory given by waypoints in cartesian coordinates
           waypoints is list of numpy array of coordinates if form P = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)
           After execution waits 0.4s to make sure the robot arrived to destination pose.
           returns True if succeeded, else returns False"""
        way = []
        pos = self.arm.get_current_pose().pose
        for w in waypoints:
            q = tft.quaternion_from_euler(w[5][0],w[4][0],w[3][0],axes='szxz')
            pos.position.x = w[0][0]
            pos.position.y = w[1][0]
            pos.position.z = w[2][0]
            pos.orientation.x = q[0]
            pos.orientation.y = q[1]
            pos.orientation.z = q[2]
            pos.orientation.w = q[3]
            way.append(copy.deepcopy(pos))
                
        
        (plan, fraction) = self.arm.compute_cartesian_path(way,   # waypoints to follow
                                                            0.01,        # eef_step
                                                            0.0)         # jump_threshold

        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ["j1","j2","j3","j4","j5","j6"]
        joint_state.position = self.arm.get_current_joint_values()
        moveit_robot_state = RobotState()
        moveit_robot_state.joint_state = joint_state
        plan = self.arm.retime_trajectory(moveit_robot_state, plan, self._speed)
        
        try:
            self.arm.execute(plan,wait = True)
        except Exception as e:
            rospy.logfatal(e)
            return False

        rospy.sleep(0.4)
        
        X = self.get_position()
        R1 = tft.euler_matrix(X[5][0],X[4][0],X[3][0],axes='szxz')
        R2 = tft.euler_matrix(waypoints[-1][5],waypoints[-1][4],waypoints[-1][3],axes='szxz')
        if np.all(abs(X[0:3]-waypoints[-1][0:3]) < 10**-4) and tft.is_same_transform(R1,R2):
            return True
        else:
            rospy.logerr("Something went wrong, desired end position unreached")
            return False


    def execute_joint_trajectory(self, waypoints):
        """Executes trajectory given by waypoints in joint coordinates
           waypoints is a list of joint values if form waipoints = [[J1,J2,J3,J4,J5,J6],...]
           After execution waits 0.4s to make sure the robot arrived to destination pose.
           returns True if succeeded, else returns False"""
        self.arm.set_joint_value_target(waypoints[0][0:6])
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ["j1","j2","j3","j4","j5","j6"]
        moveit_robot_state = RobotState()
        moveit_robot_state.joint_state = joint_state
        joint_state.position = self.arm.get_current_joint_values()
        self.arm.set_start_state(moveit_robot_state)
        plans = self.arm.plan()
        joint_state.position = waypoints[0][0:6]
        self.arm.set_start_state(moveit_robot_state)
        plan = self.arm.plan()
        plans.joint_trajectory.points += plan.joint_trajectory.points
        for w in range(len(waypoints)):
            if w == 0: 
                continue
            self.arm.clear_pose_targets()
            self.arm.set_joint_value_target(waypoints[w][0:6])
            plan = self.arm.plan()
            plans.joint_trajectory.points += plan.joint_trajectory.points

            joint_state.position = waypoints[w][0:6]
            moveit_robot_state = RobotState()
            moveit_robot_state.joint_state = joint_state
            self.arm.set_start_state(moveit_robot_state)


        plans = self.arm.retime_trajectory(moveit_robot_state, \
                                           plans, \
                                           self._speed)

        try:
            self.arm.execute(plans, wait=True)
        except Exception as e:
            rospy.logfatal(e)
            return False
        
        rospy.sleep(0.4)

        if np.all(np.array(self.arm.get_current_joint_values()) - np.array(waypoints[-1][0:6]) <= 1*10**(-3)):
            return True
        else:
            return False

    def get_transform_matrix(self, frame1, frame2):
        (trans,rot) = self.listener.lookupTransform(frame1, frame2, rospy.Time(0))
        R = tft.quaternion_matrix(rot)
        t = tft.compose_matrix(translate = trans)
        return np.matmul(t,R)

    def dkt(self, J):
        """Returns cartesian position of end-point of the robot for given joint values in form J = [J1,J2,J3,J4,J5,J6]
        output is in form in form X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]])"""
        self.kin_solver.base_matrix = self.get_transform_matrix('world', self.kin_config['base_robot_frame'])
        self.kin_solver.eef_matrix = self.get_transform_matrix(self.kin_config['last_robot_frame'], self.kin_config['eef_robot_frame'])
        X = self.kin_solver.dkt(J)
        return X

    def ikt(self, X):
        """Returns list all joint coordinates to reach given position in form X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)
           if soluion exists the output has form J = [[J1,J2,J3,J4,J5,J6],...]
           if infinity solution exists, the joint value, for which infinity solutions exists is marked with char 'i'
           (f.e.: J = [[J1,J2,J3,'i',J5,'i'],...])
           if no solution exists returns empty list
           this function ignores collisions!"""
        self.kin_solver.base_matrix = self.get_transform_matrix('world', self.kin_config['base_robot_frame'])
        self.kin_solver.eef_matrix = self.get_transform_matrix(self.kin_config['last_robot_frame'], self.kin_config['eef_robot_frame'])
        J = self.kin_solver.ikt(X)
        return J
    
    def inf_ikt(self, X, J):
        """Returns one solution in case of infinity solutions for position X in fom X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)
           input J is list of joint values in form J=[J1,J2,J3,J4,J5,J6], where one of joint variables is marked with 'i' for which solution is to be found
           in list J can be only one 'i'
           if no solution is found or the input is incorrect returns empty list, else returns list of joint values in form J=[J1,J2,J3,J4,J5,J6]
        """
        J = self.kin_solver.ik_for_inf(X, J)
        return J

    def spawn_box(self, name, size, position):
        """Spawns box of given size and name to given position
           size is a list of three ints or three floats
           position is in form P = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)
"""
        box_pose = geometry_msgs.msg.PoseStamped()
        box_pose.header.frame_id = "world"
        box_pose.header.seq = 0
        box_pose.header.stamp = rospy.Time.now()
        box_pose.pose.position.x = position[0][0]
        box_pose.pose.position.y = position[1][0]
        box_pose.pose.position.z = position[2][0]
        q = tft.quaternion_from_euler(position[5][0], position[4][0], position[3][0], axes ='szxz')
        box_pose.pose.orientation.x = q[0] 
        box_pose.pose.orientation.y = q[1]       
        box_pose.pose.orientation.z = q[2]
        box_pose.pose.orientation.w = q[3]
        if len(size) != 3:
            return False
        self.scene.add_box(name, box_pose, size)
        return True

    def spawn_sphere(self, name, radius, position):
        """Spawns sphere of given name and radius to given position
           radius is float or int
           position is in form P = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)
"""
        sphere_pose = geometry_msgs.msg.PoseStamped()
        sphere_pose.header.frame_id = "world"
        sphere_pose.header.seq = 0
        sphere_pose.header.stamp = rospy.Time.now()
        sphere_pose.pose.position.x = position[0][0]
        sphere_pose.pose.position.y = position[1][0]
        sphere_pose.pose.position.z = position[2][0]
        q = tft.quaternion_from_euler(position[5][0], position[4][0], position[3][0], axes ='szxz')
        sphere_pose.pose.orientation.x = q[0] 
        sphere_pose.pose.orientation.y = q[1]       
        sphere_pose.pose.orientation.z = q[2]
        sphere_pose.pose.orientation.w = q[3]
        
        self.scene.add_sphere(name, sphere_pose, radius)
        return True

    def attach_object_to_gripper(self, name):
        """Attaches body to gripper
           returns True if succedded, else returns False"""
        if self.gripper:
            grasping_group = 'hand'
            touch_links = self.robot.get_link_names(group=grasping_group)
            #print touch_links
            try:
                self.scene.attach_box('planning_tip', name, touch_links=touch_links)
            except Exception as e:
                rospy.logfatal(e)
                return False
            return True
        else:
            rospy.loger("ERROR: No gripper, object cannot be gripped")
            return False

    def deattach_object_from_gripper(self, name):
        """Deattaches body from gripper
           returns True if succedded, else returns False"""
        try:
            self.scene.remove_attached_object('planning_tip', name)
        except Exception as e:
            rospy.logfatal(e)
            return False
        return True

    def remove_object(self, name):
        """removes spawned body of given name
           returns True if succedded, else returns False"""
        try:
            self.scene.remove_world_object(name)
        except Exception as e:
            rospy.logfatal(e)
            return False
        return True
    
    @property
    def max_speed(self):
        return self._max_speed
    
    def speed(self):
        return self._speed

if __name__ == "__main__":
    robot = Mitsubishi_robot()
    robot.set_max_speed(0.3)
    J = [[0,0,0,0.1,0,0]]
    for j in J:
        print(j)
        print('dkt')
        print(robot.dkt(j))
        print
        robot.set_joint_values(j)


