#!/usr/bin/python
import sys
import copy
#import rospy
from math import pi
import numpy as np
import tf.transformations as tft

class KIN_6DOF():
    def __init__(self, lens, joint_limits, eef_transform):
        """Kinemateics object initialization, lens is a list of six link lenths, 
        joint_limits is list of joint limits in form [(min(J1),max(J1)),((min(J2),max(J2)),(min(J3),max(J3)),(min(J4),max(J4)),(min(J5),max(J5)),(min(J6),max(J6))]
        eef_transform is a transformation matix from link 6 to the end effector system"""
        self.lens = lens
        self.joint_limits = joint_limits
        self.eef_transform = eef_transform
        self.l54 = (self.lens[4]**2 + self.lens[3]**2)**0.5
        self.l43 = (self.lens[2]**2 - (self.lens[3] - self.lens[1])**2)**0.5
        self.j1c = np.arcsin(self.l43/self.lens[2])

    def to_npi_pi(self, j):
        if j > pi:
            j = -2*pi+j
        elif j < -pi:
            j = 2*pi+j
        return j
    
    def to_2pi(self,j):
        return (j/(2*pi)-j//(2*pi))*2*pi

    def get_R03(self, J): 
        R03 = self.trans_from_DH(J[0], 0, 0, pi/2)
        R03 = np.matmul(R03,self.trans_from_DH(pi/2-J[1], 0, 0, 0))
        R03 = np.matmul(R03,self.trans_from_DH(pi/2-J[2], 0, 0, pi/2))
        return R03
    
    def get_T06(self, X):
        R0g = tft.euler_matrix(X[5][0],X[4][0],X[3][0],axes='szxz')
        t0g = tft.compose_matrix(translate=[X[0][0],
                                            X[1][0],
                                            X[2][0]])
        T06 = tft.concatenate_matrices(t0g,R0g,np.linalg.inv(self.eef_transform))
        return T06
    
    def get_j46(self, R03, T06):
        J46 = []
        j46 = []
        R03 = R03[0:3, 0:3]
        R06 = T06[0:3, 0:3]
        j46 = self.J_from_R(np.matmul(R03.T,R06))
        J46.append(copy.deepcopy(j46))
        j46[0] += pi
        j46[1] *= -1
        j46[2] += pi
        for u in range(3):
            j46[u] = self.to_npi_pi(j46[u])
        J46.append(copy.deepcopy(j46))
        return J46
    
    def remove_OOR_add_IR_sol(self, J):
        indexes_to_keep = []
        for i in range(0,len(J)):
            out_of_range = False
            for u in range(len(J[i])):
                if J[i][u] < self.joint_limits[u][0] or J[i][u] > self.joint_limits[u][1]:
                    out_of_range = True
                    continue
            if not out_of_range:
                indexes_to_keep.append(i)
        Jfin = []
        #DONE: MAKE it for all joints
        for i in indexes_to_keep:
            Jr = []
            for u in range(6):
                Jr.append(np.concatenate((np.arange(J[i][u], np.nextafter(self.joint_limits[u][0], self.joint_limits[u][0]-1),-2*pi)[1:],
                                          np.arange(J[i][u], np.nextafter(self.joint_limits[u][1], self.joint_limits[u][1]+1), 2*pi))))
            Jf = np.array(np.meshgrid(Jr[0],Jr[1],Jr[2],Jr[3],Jr[4],Jr[5])).T.reshape(-1,6)
            Jfin += Jf.tolist()
        return Jfin
    
    def J_from_R(self, R):
        J = [None, None, None]
        if (abs(abs(R[2,2])-1)>10**(-16)):
            J[1] = np.arccos(R[2,2])
            J[2] = np.arctan2(-np.sin(J[1])*R[2,0],-np.sin(J[1])*R[2,1])
            J[0] = np.arctan2(-np.sin(J[1])*R[1,2],-np.sin(J[1])*R[0,2])
        else:
            if (R[2,2]>0):
                J[1] = 0;
                J[0] = np.arctan2(-R[1,1], -R[0,1]);
                J[2] = 0;
            else:
                J[1] = pi;
                J[0] = np.arctan2(R[1,1], R[0,0]);
                J[2] = 0;
        return J
    
    def trans_from_DH(self, theta, d, a, alpha):
        return np.array([[np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
                         [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
                         [0, np.sin(alpha), np.cos(alpha), d],
                         [0, 0, 0, 1]])
    
    def ikt(self, X):
        """Returns list all joint coordinates to reach given position in form X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]])
           if soluion exists the output has form J = [[J1,J2,J3,J4,J5,J6],...]
           if infinity solution exists, the joint value, for which infinity solutions exists is marked with char 'i'
           (f.e.: J = [[J1,J2,J3,'i',J5,'i'],...])
           if no solution exists returns empty list
           this function ignores collisions!"""
        #Returns joint coordinates to get the end effector to position X
    
        def ikt3(W):
            #Returns joint coordinates for lower 3 joints
            J = []
            W = np.array(W)
            O = np.array([[0],[0],[0]])
            None_point = np.array([[None],[None],[None]])
    
            Wxy = copy.deepcopy(W)         # point w in plain XY
            Wxy[2] = 0
                
            if Wxy[0] == 0 and Wxy[1] == 0:
                A1 = np.array([[self.lens[1]],[0],[0]]) + np.array([[0],[0],[self.lens[0]]])
                A2 = -np.array([[self.lens[1]],[0],[0]]) + np.array([[0],[0],[self.lens[0]]])
            else:
                A1 = Wxy/np.linalg.norm(Wxy)*self.lens[1] + np.array([[0],[0],[self.lens[0]]])
                A2 = -Wxy/np.linalg.norm(Wxy)*self.lens[1] + np.array([[0],[0],[self.lens[0]]])
    
    
            a = [A1, A2]
            b = [[None_point,None_point],[None_point,None_point]]
                
    
            WA1 = A1 - W
            WA2 = A2 - W
            Wa = [WA1, WA2]   # WA vectors
    
            D = [np.linalg.norm(WA1), np.linalg.norm(WA2)]  # Distances WA
    
            z = np.array([[0],[0],[1]])
    
            beta = np.arccos(self.lens[3]/self.l54)
            sol_iter = 0
            for i in range(2):  # for those 2 versions of point A
                A = a[i]
                WA = Wa[i]
                d = D[i]
                # Divide accoarding to possible sollution
                if d > self.l54 + self.lens[2] or self.l54 > d + self.lens[2] or self.lens[2] > self.l54 + d: # Triangle inequality must be statisfied (else no solution) 
                    continue
                elif abs(d - (self.lens[2] + self.l54)) <= 10**(-6):  # one solution for B[i]
                    b[i][0] = W + WA/np.linalg.norm(WA)*self.l54
    
                elif d < (self.lens[2] + self.l54): # two possible solutions for B[i]
                    cos_alpha =  (self.l54**2 + d**2 - self.lens[2]**2) / (2*self.l54*d) 
                    alpha = np.arccos(cos_alpha)
                    h = self.l54 * np.sin(alpha)
                    h1 = self.l54*cos_alpha
                    n = np.reshape(np.cross(np.reshape(A,(1,3)), np.reshape(z,(1,3))), (3,1))
                    p = np.reshape(np.cross(np.reshape(n,(1,3)), np.reshape(WA,(1,3))), (3,1))  # velcor normal to WA in the plain genrated by A (or W or WA) and Z axis
    
                    b[i][0] = W + WA/np.linalg.norm(WA)*h1 + p/np.linalg.norm(p)*h
                    b[i][1] = W + WA/np.linalg.norm(WA)*h1 - p/np.linalg.norm(p)*h
                    
                for u in range(2):
                    if np.any(b[i][u] == None):
                        continue
                    ab = b[i][u] - A
                    bw = W-b[i][u]
                    j1 = np.arctan2(A[1], A[0])
                    Axy = np.matmul([[1,0,0],[0,1,0],[0,0,0]],A)
                    Bxy = np.matmul([[1,0,0],[0,1,0],[0,0,0]],b[i][u])
                    bwxy = np.matmul([[1,0,0],[0,1,0],[0,0,0]],bw)
                            
                    Aq = np.array([(A[0]**2+A[1]**2)**0.5,A[2]])
                    if np.all(abs(Axy/np.linalg.norm(Axy) - Bxy/np.linalg.norm(Bxy)) <= 10**(-10)):
                        Bq = np.array([(b[i][u][0]**2+b[i][u][1]**2)**0.5,b[i][u][2]])
                    else:
                        Bq = np.array([-(b[i][u][0]**2+b[i][u][1]**2)**0.5,b[i][u][2]])
                    if np.all(abs(Axy/np.linalg.norm(Axy) - Wxy/np.linalg.norm(Wxy)) <= 10**(-10)):
                        Wq = np.array([(W[0]**2+W[1]**2)**0.5,W[2]])
                    else:
                        Wq = np.array([-(W[0]**2+W[1]**2)**0.5,W[2]])
                        
                    ABq = Bq-Aq
                    BWq = Wq-Bq
                    j2 = pi/2 - np.arctan2(ABq[1],ABq[0])
                    j2 = self.to_npi_pi(j2)
                    if j2 >= 0:
                        gama = pi-j2
                    else:
                        gama = -pi-j2
                    theta = np.arctan2(BWq[1],BWq[0])
                    j3 = gama - theta - beta 
                    j3 = self.to_npi_pi(j3)
                    J.append([j1[0],j2[0],j3[0]])
            return J
    
        #The IKT starts here
    
        J = []
        T06 = self.get_T06(X)
        t67 = tft.compose_matrix(translate=[0,
                                            0,
                                            -self.lens[5]]) 
    
        X6 = np.array([[0],[0],[0],[1]])
        W = np.matmul(np.matmul(T06,t67),X6)
        J3 = ikt3(W[0:3])
        for j in J3:
            J.append(copy.deepcopy(j))
            J.append(copy.deepcopy(j))
        J46 = []
        for i in range(len(J3)):
            R03 = self.get_R03(J3[i])
            J46 += self.get_j46(R03, T06)
        for i in range(len(J)):
            J[i] += J46[i]
        # romove solutions out of range and add in range solutions
        Jfin = self.remove_OOR_add_IR_sol(J)
    
        # Mark infinity solutions
        a = (self.lens[2]**2 - (self.lens[3] - self.lens[1])**2)**0.5
        for j in Jfin:
            if j[4] == 0:   # J6 and J4 in one axis 
                j[3] = 'i'
                j[5] = 'i'  
            if j[1] == self.j1c and j[2] == -j[1]:  # if J4 and J1 in one axis
                j[0] = 'i'
                j[3] = 'i'
            if X[0] == 0 and X[1] == 0 and W[0] == 0 and W[0] == 0: # if J6 and J1 on one axis
                j[0] = 'i'
                j[5] = 'i'
            elif W[0] == 0 and W[1] == 0:   # if W on J1 axis
                j[0] = 'i'
                j[3] = 'i'
                j[4] = 'i'
                j[5] = 'i'  
            
        return Jfin
    
    def ik_6DOF(self, X):
        return self.ikt(self, X)    
        
    
    def ik_for_inf(self, X, J):
        """Returns one solution in case of infinity solutions for position X in fom X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)
           input J is list of joint values in form J=[J1,J2,J3,J4,J5,J6], where one of joint variables is marked with 'i' for which solution is to be found
           in list J can be only one 'i'
           if no solution is found or the input is incorrect returns empty list, else returns list of joint values in form J=[J1,J2,J3,J4,J5,J6]"""
        ret = []
        X[3][0] = self.to_npi_pi(self.to_2pi(X[3][0]))
        X[4][0] = self.to_npi_pi(self.to_2pi(X[4][0]))
        X[5][0] = self.to_npi_pi(self.to_2pi(X[5][0]))
        i_found = False
        for i in range(6):
            if J[i] == 'i':
                if not i_found:
                    i_found = True
                else:
                    print('IK ERROR: Unsupported input for infinty solution to decide')
                    return ret
                continue
            J[i] = self.to_npi_pi(self.to_2pi(J[i]))

        if J[1] == 'i' or J[2] == 'i' or J[4] == 'i':
            print('IK ERROR: Unsupported input for infinty solution to decide')
        elif J[5] == 'i': 
            try:
                j5 = 0
                add = False
                if J[4] == 0 or (J[1] == self.j1c and J[2] == -J[1]):
                    j5 += X[3][0] + X[5][0] - J[3] - J[0] + pi/2
                    add = True
                #if J[1] == self.j1c and J[2] == -J[1]:  # if J4 and J1 in one axis
                #    j5 += X[3][0] - J[0] + pi/2
                #    add = True
                print(j5)
                if add:
                    J[5] = self.to_npi_pi(j5)
                    ret = self.remove_OOR_add_IR_sol([J])
                else:
                    print('IK ERROR: Unsupported input for infinty solution to decide')
                    ret = []
            except Exception as e:
                print(e)
                print('IK ERROR: Unsupported input for infinty solution to decide')
    
        elif J[3] == 'i':
            try:
                j3 = 0
                add = False
                if J[4] == 0 or (J[1] == self.j1c and J[2] == -J[1]):
                    j3 += X[3][0] + X[5][0] - J[3] - J[0] + pi/2
                    add = True
               # if J[1] == self.j1c and J[2] == -J[1]:  # if J4 and J1 in one axis
               #     j3 += X[3][0] - J[0] + pi/2
               #     add = True
                if add:
                    J[3] = self.to_npi_pi(j3)
                    ret = self.remove_OOR_add_IR_sol([J])
                else:
                    print('IK ERROR: Unsupported input for infinty solution to decide')
                    ret = []
            except Exception as e:
                print(e)
                print('IK ERROR: Unsupported input for infinty solution to decide')
    
        elif J[0] == 'i':
            try:
                j0 = 0
                add = False
                if J[4] == 0 or (J[1] == self.j1c and J[2] == -J[1]):
                    j0 += X[3][0] + X[5][0] - J[3] - J[0] + pi/2
                    add = True
                #if J[1] == self.j1c and J[2] == -J[1]:  # if J4 and J1 in one axis
                #    j0 += X[3][0] - J[3] + pi/2
                #    add = True
                if add:
                    J[0] = self.to_npi_pi(j0)
                    ret = self.remove_OOR_add_IR_sol([J])
                else:
                    print('IK ERROR: Unsupported input for infinty solution to decide')
                    ret = []
            except Exception as e:
                print(e)
                print('IK ERROR: Unsupported input for infinty solution to decide')
        else:
            print('IK ERROR: Unsupported input for infinty solution to decide')
        return ret


    def dkt(self, J):
        """Returns cartesian position of end-point of the robot for given joint values in form J = [J1,J2,J3,J4,J5,J6]
        output is in form in form X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)"""
        T = self.dkt_get_T(J,7)
        X = np.matmul(T,np.array([[0],[0],[0],[1]]))
        X = X[0:3]
        R = copy.deepcopy(T)
        R[0:3, 3] = 0
        R = tft.euler_from_matrix(R, 'szxz')
        R = np.reshape(R,(3,1))
        R = np.flip(R)
        X = np.concatenate((X,R),axis=0)
        return X

    def dkt_get_T(self, J, n):
        '''Returns transformation matric from world frame to n-th frame (n: 0 - base link, 7 - eef)
        J has form of [J1,J2,J3,J4,J5,J6]
        output is in form in form X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotation)'''
        T = np.eye(4)
        if n == 0:
            return T
        T = np.matmul(T, self.trans_from_DH(J[0], self.lens[0], self.lens[1], pi/2))
        if n == 1:
            return T
        T = np.matmul(T,self.trans_from_DH(pi/2-J[1], 0, self.lens[2], 0))
        if n == 2:
            return T
        T = np.matmul(T,self.trans_from_DH(pi/2-J[2], 0, self.lens[3], pi/2))
        if n == 3:
            return T
        T = np.matmul(T,self.trans_from_DH(J[3], self.lens[4], 0, pi/2))
        if n == 4:
            return T
        T = np.matmul(T,self.trans_from_DH(J[4], 0, 0, -pi/2))
        if n == 5:
            return T
        T = np.matmul(T,self.trans_from_DH(J[5]+pi/2, self.lens[5], 0, 0))
        if n == 6:
            return T
        T = np.matmul(T,self.eef_transform)
        if n == 7:
            return T


    def dkt_to_system(self, J, n):
        '''Solves direct kinematics in world system to n-th system (n: 0 - base link, 7 - eef),
        J has form of [J1,J2,J3,J4,J5,J6]
        output is in form in form X = numpy.array([[X],[Y],[Z],[Rz1],[Rx],[Rz2]]) (Euler angles rotion)'''
        T = self.dkt_get_T(J,n)
        X = np.matmul(T,np.array([[0],[0],[0],[1]]))
        X = X[0:3]
        R = copy.deepcopy(T)
        R[0:3, 3] = 0
        R = tft.euler_from_matrix(R, 'szxz')
        R = np.reshape(R,(3,1))
        R = np.flip(R)
        X = np.concatenate((X,R),axis=0)
        return X
            

