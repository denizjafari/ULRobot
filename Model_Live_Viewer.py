import pandas as pd
from matplotlib.animation import FuncAnimation
from Plot3D import *
import sys

sys.path.append('/home/scott/PycharmProjects/pythonProject')
sys.path.append('/home/scott/Python')
has_been_zeroed = False


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=113, azim=180, roll=0)
plt.style.use('fast')
index = count()  # Variable for each animation iteration
Axes.arrow_heads = [ax.quiver(0, 0, 0, 0, 0, 0, color=color, arrow_length_ratio=0.1) for color in Axes.colors]
Height = 1800  # Patient height in millimetres

### ADD AXES AND LINKS ###
axes0 = Axes('GC')  # Add global coordinate axes
axes1 = Axes('AX1')  # Add GH joint coordinates

L0 = Links('Shoulder')  # Define stationary shoulder-spine
L0.Length = Height * 0.129  # Length based on Drillis and Contini 1966 as a function of height
L0.Position1 = [0, 0, L0.Length]
L0.Position2 = [0, 0, 0]
L0.is_rigid = True  # Defines link as fixed  # Define shoulder link as per kinematics

L1 = Links('Humerus')  # Define L1 as humerus
L1.Alignment = [-1, 'x']
L1.Length = Height * (0.818 - 0.63)  # Length based on Drillis and Contini 1966 as a function of height

L2 = Links('Forearm')  # Define L2 as forearm
L2.Length = Height * (0.63 - 0.485)  # Length based on Drillis and Contini 1966 as a function of height

L3 = Links('Hand')  # Define L3 as hand
L3.Length = Height * (0.485 - 0.377)  # Length based on Drillis and Contini 1966 as a function of height

for link in Links:
    for line in link.lines:
        ax.add_line(line)
for axis in Axes:
    for line in axis.lines:
        ax.add_line(line)

for label, offset in zip(axes0.labels, axes0.label_offsets):
    ax.text(offset[0], offset[1], offset[2], label, color='k', fontsize=12)


def updates(i):
    update_lines()
    if not Axes.has_been_zeroed:
        while True:
            update_lines()
            user_input = input("Enter zero to set inverse matrices values: ")
            if user_input.lower() == 'zero':
                set_to_zero()
                Axes.has_been_zeroed = True
                break


def update_lines():
    for link, axis in zip(Links, Axes):
        if axis.is_global:
            for j, (line) in enumerate(axis.lines):
                line.set_data([0, axis.xx[j]], [0, axis.yy[j]])
                line.set_3d_properties([0, axis.zz[j]])
        if not axis.is_global:
            data = pd.read_csv(axis.filename, skiprows=[1])
            q0 = data['q0']
            q1 = data['q1']
            q2 = data['q2']
            q3 = data['q3']
            length = len(q0) - 1
            axis.q0, axis.q1, axis.q2, axis.q3 = q0[length], q1[length], q2[length], q3[length]
            axis.update_cosines(axis.q0, axis.q1, axis.q2, axis.q3)
            axis.xf = axis.cos_matrix[0, 0:3] * 100
            axis.yf = axis.cos_matrix[1, 0:3] * 100
            axis.zf = axis.cos_matrix[2, 0:3] * 100

            for j, (line) in enumerate(axis.lines):
                line.set_data([link.Position1[0], axis.xf[j]], [link.Position1[1], axis.yf[j]])
                line.set_3d_properties([link.Position1[2], axis.zf[j]])

        if link.is_rigid:
            for j, (line) in enumerate(link.lines):
                line.set_data([link.Position1[0], link.Position2[0]], [link.Position1[1], link.Position2[1]])
                line.set_3d_properties([link.Position1[2], link.Position2[2]])

        if not link.is_rigid:
            link.Alignment = [-1, 'x']
            if link.Alignment[1] == 'x':
                link.Position2 = [x * link.Length * link.Alignment[0] / 100 for x in
                                  [axis.xf[0], axis.yf[0], axis.zf[0]]]
            if link.Alignment[1] == 'y':
                link.Position2 = [x * link.Length * link.Alignment[0] / 100 for x in
                                  [axis.xf[1], axis.yf[1], axis.zf[1]]]
            if link.Alignment[1] == 'z':
                link.Position2 = [x * link.Length * link.Alignment[0] / 100 for x in
                                  [axis.xf[2], axis.yf[2], axis.zf[2]]]
            for j, (line) in enumerate(link.lines):
                line.set_data([link.Position1[0], link.Position2[0]], [link.Position1[1], link.Position2[1]])
                line.set_3d_properties([link.Position1[2], link.Position2[2]])




def set_to_zero():
    for axis in Axes:
        print(axis.cos_matrix)
        axis.inverse_matrix = np.linalg.inv(axis.cos_matrix)


# ani = FuncAnimation(fig, update_lines, interval=20, blit=True)
ani = FuncAnimation(fig, updates, interval=20, blit=True)
ax.set_xticks(np.arange(-1000, 1000, 50)), ax.set_yticks(np.arange(-1000, 1000, 50)), ax.set_zticks(
    np.arange(-1000, 1000, 50))
ax.set_xlabel('x', fontsize=10), ax.set_ylabel('y', fontsize=10), ax.set_zlabel('z', fontsize=10)
ax.set_xlim(-100, 100), ax.set_ylim(-100, 100), ax.set_zlim(-100, 100)

plt.show()
