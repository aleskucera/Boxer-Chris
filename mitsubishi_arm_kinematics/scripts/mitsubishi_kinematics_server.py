#!/usr/bin/python
import sys
import copy
import rospy
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
import numpy as np
import tf.transformations as tft
from std_msgs.msg import String
from std_msgs.msg import Header
from moveit_msgs.msg import RobotState
from moveit_msgs.msg import MoveItErrorCodes
from moveit_msgs.srv import GetPositionIK
from moveit_msgs.msg import PositionIKRequest
from sensor_msgs.msg import JointState
from moveit_msgs.srv import GetStateValidityRequest, GetStateValidity

from kinematics_6dof.kinematics_6dof import KIN_6DOF

def ikt_handle(req):
    err = MoveItErrorCodes()
    current_joint_state = req.ik_request.robot_state.joint_state.position[0:6]
    avoid_collisions = req.ik_request.avoid_collisions
    q = [req.ik_request.pose_stamped.pose.orientation.x,
         req.ik_request.pose_stamped.pose.orientation.y,
         req.ik_request.pose_stamped.pose.orientation.z,
         req.ik_request.pose_stamped.pose.orientation.w]

    r = tft.euler_from_quaternion(q, axes='szxz')
    X = np.array([[req.ik_request.pose_stamped.pose.position.x],
                  [req.ik_request.pose_stamped.pose.position.y],
                  [req.ik_request.pose_stamped.pose.position.z],
                  [r[2]],
                  [r[1]],
                  [r[0]]])

    #DONE: INFINITY solutions?!
    sol = ik_6dof.ikt(X)
    min_div = np.inf
    solution = None
    rs = copy.deepcopy(req.ik_request.robot_state)
    rs.joint_state.position = list(rs.joint_state.position)
    for s in sol:
        if 'i' in s:
            print 'i detected'
            if s[0] == 'i':
                s[0] = current_joint_state[0]
                # sol += ik_6dof.ik_for_inf(X,s)
            if s[3] == 'i':
                s[3] = current_joint_state[3]
                # sol += ik_6dof.ik_for_inf(X,s)
            sol += ik_6dof.ik_for_inf(X,s)
            continue
        rs.joint_state.header.stamp = rospy.Time.now()
        rs.joint_state.position[0:6] = s[:]
        if np.linalg.norm(np.array(s)-np.array(current_joint_state)) < min_div:
            solution = copy.deepcopy(s)
            min_div = np.linalg.norm(np.array(s)-np.array(current_joint_state))
    if solution == None:
        err.val = err.NO_IK_SOLUTION
        solution = [0.0]*6
    else:
        err.val = err.SUCCESS
    rs.joint_state.position[0:6] = solution[:]
    rs.joint_state.header.stamp = rospy.Time.now()
    return rs, err



def kinematics_server():
    rospy.init_node('mitsubishi_kinematics_server')
    s = rospy.Service('solve_ik', GetPositionIK, ikt_handle)
    rospy.spin()




if __name__ == "__main__":
    # Load robot joint limits format: list of tupples (min, max)
    joint_limits = []
    for i in range(1,7):
        maximal = float( rospy.get_param(str("/robot_description_planning/joint_limits/j"+str(i)+"/max_position")) )
        minimal = float( rospy.get_param(str("/robot_description_planning/joint_limits/j"+str(i)+"/min_position")) )
        joint_limits.append( (minimal,maximal) )
        
    # Load link lengths
    lens = []
    for i in range(1,7):
        lens.append( float( rospy.get_param(str("/Mitsubishi_robot/len_of_link"+str(i))) ) )

    # Try load schunk gripper joint limints
    gripper = False
    gripper_cont = False
    eef_len = 0
    eef_rot = np.eye(3)
    eef_transform = np.eye(4)
    eef_trans = np.zeros((3,1))
    try:
        eef_len = float( rospy.get_param(str("/Mitsubishi_robot/len_of_gripper")) )
        eef_trans[2][0] = eef_len
        eef_transform[2][3] = eef_len
    except Exception as e:
        rospy.logfatal(str("Exception: " + str(e)))

    ik_6dof = KIN_6DOF(lens, joint_limits, eef_transform)
    kinematics_server()
