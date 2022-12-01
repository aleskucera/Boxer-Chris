'''
Title: cube_2.py
Author: Roid Maulana
Description: Demonstrating Python Libraries to produce vertices of a cube with rotational animation
             Feel free to improve by forking this repository and submitting pull requests if needed. Happy hacking :)
License:  GNU GENERAL PUBLIC LICENSE 3.0
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
import cv2

matplotlib.use('TkAgg')


class Cube:
    def __init__(self, size=1, center=(0, 0, 0)):
        self.size = size
        self.center = center
        self.rotation = [0, 0, 0]
        self.vertices = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1]
        ]) * size + center

        self.names = ['A', 'B', 'D', 'C', 'E', 'F', 'H', 'G']

        self.edges = np.array([
            [0, 1],
            [0, 2],
            [0, 4],
            [1, 3],
            [1, 5],
            [2, 3],
            [2, 6],
            [3, 7],
            [4, 5],
            [4, 6],
            [5, 7],
            [6, 7]
        ])

        self.faces = np.array([
            [0, 1, 3, 2],
            [0, 1, 5, 4],
            [0, 2, 6, 4],
            [1, 3, 7, 5],
            [2, 3, 7, 6],
            [4, 5, 7, 6]
        ])

        self.colors = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ])

    def rotate(self, x=0, y=0, z=0):
        self.rotation = [x, y, z]
        self.vertices = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1]
        ]) * self.size + self.center

        self.vertices = self.rotate_x(self.vertices, x)
        self.vertices = self.rotate_y(self.vertices, y)
        self.vertices = self.rotate_z(self.vertices, z)

    @staticmethod
    def rotate_x(vertices, angle):
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
        return np.dot(vertices, rotation_matrix)

    @staticmethod
    def rotate_y(vertices, angle):
        rotation_matrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
        return np.dot(vertices, rotation_matrix)

    @staticmethod
    def rotate_z(vertices, angle):
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        return np.dot(vertices, rotation_matrix)

    @property
    def outer_vertices(self):
        # return vertices that are between maximum and minimum of z value
        z = self.vertices[:, 2]

        # if maximum has 4 vertices, then it is a face that is facing the camera
        if np.sum(z == np.max(z)) == 4:
            return self.vertices[z == np.max(z)]
        return self.vertices[(z > np.min(z)) & (z < np.max(z))]

    @property
    def outer_edges(self):
        # return edges that are between maximum and minimum of z value
        z = self.vertices[:, 2]
        max_z = np.max(z)
        min_z = np.min(z)
        n_max_z = np.sum(z == max_z)
        if n_max_z == 4:
            # if maximum has 4 vertices, then it is a face that is facing the camera
            # return edges that are connected to the vertices that are facing the camera
            return self.edges[np.any(np.isin(self.edges, np.where(z == max_z)), axis=1)]
        if n_max_z == 2:
            # if maximum has 2 vertices, then it is an edge that is facing the camera
            # return all edges that are not between the vertices that are facing the camera
            max_edge = self.edges[np.all(np.isin(self.edges, np.where(z == max_z)), axis=1)]
            min_edge = self.edges[np.all(np.isin(self.edges, np.where(z == min_z)), axis=1)]

            # return edges that are not equal to max_edge and min_edge
            return self.edges[np.any(np.logical_not(np.isin(self.edges, np.concatenate((max_edge, min_edge)))), axis=1)]
        else:
            return self.edges[(z[self.edges[:, 0]] > np.min(z)) & (z[self.edges[:, 0]] < np.max(z)) & (
                    z[self.edges[:, 1]] > np.min(z)) & (z[self.edges[:, 1]] < np.max(z))]


def convex_hull_2d():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    cube = Cube(size=1, center=(0, 0, 0))
    cube.rotate(x=10 * np.pi / 180, y=10 * np.pi / 180, z=10 * np.pi / 180)

    # Add vertices with names
    for vertex, name in zip(cube.vertices, cube.names):
        ax.scatter(vertex[0], vertex[1], color='r')
        ax.text(vertex[0] + 0.05, vertex[1], name, fontsize=15)

    # Create convex hull around the vertices
    hull = cv2.convexHull(cube.vertices[:, :2].astype(np.float32))
    hull = np.concatenate((hull, hull[:1]))
    hull = hull.reshape(-1, 2)
    ax.plot(hull[:, 0], hull[:, 1], color='y', linewidth=2)

    plt.show()


def draw_2d_projection():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    cube = Cube(size=1, center=(0, 0, 0))

    for edge in cube.outer_edges:
        ax.plot(cube.vertices[edge, 0], cube.vertices[edge, 1], 'b')

    def update(i):
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        cube.rotate(x=i * np.pi / 180, y=i * np.pi / 180, z=i * np.pi / 180)
        ax.clear()

        # Add vertices with names
        for vertex, name in zip(cube.vertices, cube.names):
            ax.scatter(vertex[0], vertex[1], color='r')
            ax.text(vertex[0] + 0.05, vertex[1], name, fontsize=15)

        for i, edge in enumerate(cube.outer_edges):
            ax.plot(cube.vertices[edge, 0], cube.vertices[edge, 1], 'y', linewidth=3)

    anim = FuncAnimation(fig, update, frames=360, interval=20)
    plt.show()


def draw_edges():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    cube = Cube(size=1, center=(0, 0, 0))
    ax.scatter(cube.vertices[:, 0], cube.vertices[:, 1], cube.vertices[:, 2])

    for edge in cube.edges:
        ax.plot(cube.vertices[edge, 0], cube.vertices[edge, 1], cube.vertices[edge, 2], 'b')

    def update(i):
        ax.view_init(elev=10., azim=i)

    anim = FuncAnimation(fig, update, frames=360, interval=20)
    plt.show()


def draw_vertices():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    cube = Cube(size=1, center=(0, 0, 0))
    ax.scatter(cube.vertices[:, 0], cube.vertices[:, 1], cube.vertices[:, 2])

    def update(i):
        ax.view_init(elev=10., azim=i)

    anim = FuncAnimation(fig, update, frames=360, interval=20)
    plt.show()


if __name__ == '__main__':
    convex_hull_2d()
    draw_2d_projection()
    draw_edges()
    draw_vertices()

# A = np.array([-0.5, -0.5, -0.5])
# B = np.array([0.5, -0.5, -0.5])
# C = np.array([0.5, 0.5, -0.5])
# D = np.array([-0.5, 0.5, -0.5])
# E = np.array([-0.5, -0.5, 0.5])
# F = np.array([0.5, -0.5, 0.5])
# G = np.array([0.5, 0.5, 0.5])
# H = np.array([-0.5, 0.5, 0.5])
#
# load = np.array([A, B, C, D, E, F, G, H])
# fig = plt.figure()
# ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))
#
# #   Declared to allow for x and y axis only
# projection = np.array([[1, 0, 0], [0, 1, 0]])
#
# plt.title("Render 3D Cube in 2D Space")
#
# # list of the angles in radians
# angles = np.linspace(0, 2 * np.pi, 360)
#
# # storage of single frames - one value per point and angle.
# frames = np.zeros((len(load), len(angles), 2))
#
# # loops through all points and angles to store for later usage.
# for i, x in enumerate(load):
#     for j, angle in enumerate(angles):
#         rotationY = np.array([[np.cos(angle), 0, np.sin(angle)],
#                               [0, 1, 0],
#                               [-np.sin(angle), 0, np.cos(angle)]])
#         rotationX = np.array([[1, 0, 0],
#                               [0, np.cos(angle), -np.sin(angle)],
#                               [0, np.sin(angle), np.cos(angle)]])
#         rotationZ = np.array([[np.cos(angle), -np.sin(angle), 0],
#                               [np.sin(angle), np.cos(angle), 0],
#                               [0, 0, 1]])
#         rotated = np.dot(rotationX, x)
#         rotated = np.dot(rotationY, rotated)
#         rotated = np.dot(rotationZ, rotated)
#         projected2d = np.dot(projection, rotated)
#         print(projected2d)
#         # store the point.
#         frames[i, j, :] = projected2d
#
# # draws the initial point.
# line, = ax.plot(frames[:, 0, 0], frames[:, 0, 1], c="blue", marker="o", ls='')
#
#
# # defines what happens at frame 'i' - you want to update with the current
# # frame that we have stored before.
# def animate(i):
#     line.set_data(frames[:, i, 0], frames[:, i, 1])
#     return line  # not really necessary, but optional for blit algorithm
#
#
# # the number of frames is the number of angles that we wanted.
# anim = FuncAnimation(fig, animate, interval=200, frames=len(angles))
# plt.draw()
# plt.show()
#
# '''
# The FuncAnimation constructor takes a callable function (in my case variable called animate) which
# gets the current frame number as an argument (here i) and updates the plot.
# This means, all of the intermediate points should be stored in an array (frames)
# and then later access them (possible to also compute the projection on the fly,but not recommended).
# The animation will then loop through the frames and apply the function to every frame.
# '''
