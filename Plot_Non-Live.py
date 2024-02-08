from functions import *
import matplotlib.pyplot as plt
import numpy as np


# plt.style.use('fast')
def plot():
    data = np.genfromtxt("data/data.csv", delimiter=",", skip_header=2)

    timestamp = data[:, 0]


    gyro = data[:, 4:7]
    acc = data[:, 1:4]
    mag = data[:, 7:10]
    deg = data[:, 16:18]
    quaternions = data[:, 12:16]

    figure, axes = plt.subplots(nrows=5, sharex=True, gridspec_kw={"height_ratios": [1, 1, 1, 1, 1]})
    figure.suptitle("IMU Data")
    label = ['Degrees', 'Acceleration', 'Angular Velocity', 'Magnetic Flux', 'Quaternion']
    colours = ('tab:purple', 'tab:green', 'tab:red')

    for i in range(5):
        axes[i].grid()
        axes[i].set_ylabel(label[i])

    for i in range(len(deg[0])):
        axes[0].plot(timestamp[:], deg[:, i], colours[i], label='d0', linewidth=1)
    axes[0].set_ylim([-180, 180])
    axes[0].set_ylabel("Degrees")
    axes[0].legend()

    axes[1].plot(timestamp, acc[:, 0], "tab:purple", label='x-acc', linewidth=1)
    axes[1].plot(timestamp, acc[:, 1], "tab:green", label='y-acc', linewidth=1)
    axes[1].plot(timestamp, acc[:, 2], "tab:red", label='z-acc', linewidth=1)
    axes[1].set_ylim([-20, 20])
    axes[1].legend()

    axes[2].plot(timestamp, gyro[:,0], "tab:purple", label='x-gyro', linewidth=1)
    axes[2].plot(timestamp, gyro[:,1], "tab:green", label='y-gyro', linewidth=1)
    axes[2].plot(timestamp, gyro[:,2], "tab:red", label='z-gyro', linewidth=1)
    axes[2].set_ylim([-30, 30])
    axes[2].legend()

    axes[3].plot(timestamp, mag[:,0], "tab:purple", label='x-mag', linewidth=1)
    axes[3].plot(timestamp, mag[:,1], "tab:green", label='y-mag', linewidth=1)
    axes[3].plot(timestamp, mag[:,2], "tab:red", label='z-mag', linewidth=1)
    axes[3].set_ylim([-20, 20])
    axes[3].legend()

    axes[4].plot(timestamp, quaternions[:,0], "tab:blue", label='q0', linewidth=1)
    axes[4].plot(timestamp, quaternions[:,1], "tab:purple", label='q1', linewidth=1)
    axes[4].plot(timestamp, quaternions[:,2], "tab:green", label='q2', linewidth=1)
    axes[4].plot(timestamp, quaternions[:,3], "tab:red", label='q3', linewidth=1)
    axes[4].set_ylim([-1.5, 1.5])
    axes[4].legend()

    plt.tight_layout()
    plt.grid(True)
    # if t_curr >= 15:
    #     plt.xlim(t_curr - 15, t_curr + 5)
    # else:
    #     plt.xlim(0, 20)

#estimate_sampling(timestamp)
plot()
plt.tight_layout()
plt.show()
