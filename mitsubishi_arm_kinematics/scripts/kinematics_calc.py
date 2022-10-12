#!/usr/bin/python
import sys
import copy
import rospy
from math import pi
import numpy as np
from kinematics_6dof.kinematics_6dof import KIN_6DOF


def input_to_float(s):
    s = s.split(' ')
    for i in range(len(s)):
        if '*pi' in s[i]:
            s[i] = float(s[i].split('*pi')[0])*pi
        elif 'pi' in s[i]:
            s[i] = pi
        elif s[i] == 'i':
            continue
        s[i] = float(s[i])
    return s
    


if __name__=="__main__":

    rospy.init_node('kinematics_calc')

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
    #print lens

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

    kin = KIN_6DOF(lens, joint_limits, eef_transform)

    print('\n\n\nThis tool is for solving kinematics of robotic arms RV-6S and RV-6SDL. \nPlease follow the dialogues and please use only decimal numbers and pi (f.e.: \'0.75\', \'0.75*pi\' or \'pi\').\nTo quit type \'Quit\' or \'q\' and press enter\n\nSincerely,\nyour developer')
    while(True):
        variant = raw_input("\n \nIK, DK or inf? \n")
        if variant == "I" or variant == "i" or variant == "ik" or variant == "IK":
            X = raw_input("Enter position in format 'X Y Z Ez Ex Ez' \n")
            try:
                X = input_to_float(X)
                if len(X) != 6 or 'i' in X:
                    print('ERROR invalid input')
                    continue
                X = np.array(X).reshape(6,1)
                print("IK for X = ")
                print(X)
                print ''
                print('\nSolution:')
                for j in kin.ikt(X):
                    print(j)
            except Exception as e:
                rospy.logfatal(str("Exception: " + str(e)))

        elif variant == "D" or variant == "d" or variant == "dk" or variant == "DK":
            J = raw_input("Enter joint coordinates in format 'J1 J2 J3 J4 J5 J6'\n")
            try:
                J = input_to_float(J)
                if len(J) != 6 or 'i' in J:
                    print('ERROR invalid input')
                    continue
                print("DK for J = ")
                print(J)
                print('\nSolution:')
                for j in kin.dkt(J):
                    print(j)
            except Exception as e:
                rospy.logfatal(str("Exception: " + str(e)))

        elif variant == 'inf' or variant == 'INF':
            J = raw_input("Enter joint coordinates in format 'J1 J2 J3 J4 J5 J6'\n")
            X = raw_input("Enter position in format 'X Y Z Ez Ex Ez' \n") 
            try:
                J = input_to_float(J)
                if len(J) != 6 or not 'i' in J:
                    print('ERROR invalid input')
                    continue
                X = input_to_float(X)
                if len(X) != 6 or 'i' in X:
                    print('ERROR invalid input')
                    continue
                X = np.array(X).reshape(6,1)
                print("Inf IK for J = ")
                print(J)
                print("and X = ")
                print(X)
                print('\nSolution:')
                for j in kin.ik_for_inf(X,J):
                    print(j)
            except Exception as e:
                rospy.logfatal(str("Exception: " + str(e)))


        elif variant == 'q' or variant == 'Q' or variant == 'quit' or variant == 'Quit' or variant == 'QUIT':
            break
        else:
            print 'I dunno what do ya want, but 42 might be the answer'
