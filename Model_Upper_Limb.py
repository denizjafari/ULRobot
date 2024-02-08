import numpy as np
import math
import matplotlib.pyplot as plt
from itertools import count
import pandas as pd
from matplotlib.animation import FuncAnimation

plt.style.use('fast')
index = count()
angles = np.array([0, 0, 0, 0, 0, 0, 0])  # Shoulder ABD,FLX,ROT (+ve lateral), Elbow FLX, Rad Dev, wrist ext, SUP
lengths = np.array([300, 400, 100])

data = pd.read_csv('data_test.csv', skiprows=[1])
q0 = data['q0']
q1 = data['q1']
q2 = data['q2']
q3 = data['q3']

def animate(i):
    i = next(index)
    qw = q0[i]
    qx = q1[i]
    qy = q2[i]
    qz = q3[i]
    Mat_1 = np.array([[1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qw * qz), 2 * (qx * qz + qw * qy)],
                          [2 * (qx * qy + qw * qz), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qw * qx)],
                          [2 * (qx * qz - qw * qy), 2 * (qw * qx + qy * qz), 1 - 2 * (qx * qx + qy * qy)]])
    #print(Mat_1)


    # placeholder for live data input


    #
    # if angles[6] < 90:  # Test flex ext
    #     angles[6] += 1

    # Joint positions
    # DH-Table
    T = [0, -angles[0], 90 - angles[1], angles[2], -90 - angles[3], angles[4], 90 - angles[5], -angles[6]]
    A = [-90, 90, 90, -90, -90, 90, 90, 0]
    R = [0, 0, 0, 0, -lengths[1], 0, 0, 0]
    D = [0, 0, 0, -lengths[0], 0, 0, 0, -lengths[2]]

    T = [x * math.pi / 180 for x in T]
    A = [x * math.pi / 180 for x in A]

    # Do frame zero to 1, then move forwards!!
    for i in range(len(T) - 1):
        # Allocate variables
        DH_matrix = np.zeros((4, 4))
        t2 = T[i + 1]
        a1 = A[i]
        d2 = D[i + 1]

        # Fill DH matrix
        DH_matrix[0, :] = [np.cos(t2), -np.sin(t2), 0, R[i]]
        DH_matrix[1, :] = [np.sin(t2) * np.cos(a1), np.cos(t2) * np.cos(a1), -np.sin(a1), -np.sin(a1) * d2]
        DH_matrix[2, :] = [np.sin(t2) * np.sin(a1), np.cos(t2) * np.sin(a1), np.cos(a1), np.cos(a1) * d2]
        DH_matrix[3, :] = [0, 0, 0, 1]

        if i != 0:
            DH_matrix = np.dot(DH_prev, DH_matrix)
        if i == 3:
            Elbow_position = DH_matrix
        if i == 4:
            Wrist_Position = DH_matrix
        if i == 6:
            Hand_Position = DH_matrix
        DH_prev = DH_matrix

    # Determine joint coordinates
    elb_x = Elbow_position[0, 3]
    elb_y = Elbow_position[1, 3]
    elb_z = Elbow_position[2, 3]

    wr_x = Wrist_Position[0, 3]
    wr_y = Wrist_Position[1, 3]
    wr_z = Wrist_Position[2, 3]

    hand_x = Hand_Position[0, 3]
    hand_y = Hand_Position[1, 3]
    hand_z = Hand_Position[2, 3]

    # Plot joint coordinates
    plt.cla()
    ax.plot3D([0, elb_x], [0, elb_y], [0, elb_z], 'blue', linewidth=3)
    ax.plot3D([elb_x, wr_x], [elb_y, wr_y], [elb_z, wr_z], 'red', linewidth=3)
    ax.plot3D([wr_x, hand_x], [wr_y, hand_y], [wr_z, hand_z], 'green', linewidth=3)

    x = [0, 0, 0, elb_x, elb_x, elb_x, wr_x, wr_x, wr_x, hand_x, hand_x ,hand_x]
    y = [0, 0, 0, elb_y, elb_y, elb_y, wr_y, wr_y, wr_y, hand_y, hand_y, hand_y]
    z = [0, 0, 0, elb_z, elb_z, elb_z, wr_z, wr_z, wr_z, hand_z, hand_z, hand_z]
    u = [1, 0, 0, Elbow_position[0,0], Elbow_position[0,1], Elbow_position[0,2] ,Wrist_Position[0,0], Wrist_Position[0,1], Wrist_Position[0,2],Hand_Position[0,0], Hand_Position[0,1], Hand_Position[0,2]]
    v = [0, 1, 0, Elbow_position[1,0], Elbow_position[1,1], Elbow_position[1,2] ,Wrist_Position[1,0], Wrist_Position[1,1], Wrist_Position[1,2],Hand_Position[1,0], Hand_Position[1,1], Hand_Position[1,2]]
    w = [0, 0, 1, Elbow_position[2,0], Elbow_position[2,1], Elbow_position[2,2] ,Wrist_Position[2,0], Wrist_Position[2,1], Wrist_Position[2,2],Hand_Position[2,0], Hand_Position[2,1], Hand_Position[2,2]]

    colours = ['m', 'g', 'r']
    labels = ['x', 'y', 'z']

    for i in range(len(x)):
        ax.quiver(x[i], y[i], z[i], u[i], v[i], w[i], length=50, linewidth=2.5, normalize=True, color= colours[i % 3], arrow_length_ratio=0.05)
        ax.text(x[i]+50*u[i],y[i]+50*v[i],z[i]+50*w[i],  labels[i % 3], color= colours[i % 3], fontsize = 18)

    ax.set_xticks(np.arange(-1000, 1000, 50))
    ax.set_yticks(np.arange(-1000, 1000, 50))
    ax.set_zticks(np.arange(-1000, 1000, 50))
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    ax.set_zlabel('z', fontsize=10)
    ax.set_xlim(-900, 100)
    ax.set_ylim(-100, 900)
    ax.set_zlim(-900, 100)


ani = FuncAnimation(plt.gcf(), animate, interval=50)
ax = plt.axes(projection='3d')

# ax.grid(which = 'both')
# ax.grid(which='minor', alpha = 2)
# ax.grid(which='major', alpha = 5)
ax.view_init(elev=-46, azim=1, roll=0)
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.tight_layout()
plt.show()
