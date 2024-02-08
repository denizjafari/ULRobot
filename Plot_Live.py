import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import savgol_filter

plt.style.use('fast')

def animate(i):
    data = pd.read_csv('data/data.csv', skiprows=[1])
    t_vals = data['Time_Stamp']

    d0 = data['d0']
    d1 = data['d1']
    d2 = data['d2']

    q0 = data['q0']
    q1 = data['q1']
    q2 = data['q2']
    q3 = data['q3']

    acc_x = data['ACCEL_LN_X']
    acc_y = data['ACCEL_LN_Y']
    acc_z = data['ACCEL_LN_Z']

    gyro_x = data['GYRO_X']
    gyro_y = data['GYRO_Y']
    gyro_z = data['GYRO_Z']

    mag_x = data['MAG_X']
    mag_y = data['MAG_Y']
    mag_z = data['MAG_Z']

    t_init = t_vals[0]
    last = t_vals[(t_vals.size - 1)]
    t_curr = last - t_init

    plt.cla()
    # plt.plot(t_vals, acc_x, label='x-acc', linewidth=1)
    # plt.plot(t_vals, acc_y, label='y-acc', linewidth=1)
    # plt.plot(t_vals, acc_z, label='z-acc', linewidth=1)
    # plt.ylim([-20, 20])
    # plt.xlabel("Test time (seconds)")
    # plt.ylabel("Acceleration (metres/second$^2$)")

    # plt.plot(t_vals, gyro_x, label='x-gyro', linewidth=1)
    # plt.plot(t_vals, gyro_y, label='y-gyro', linewidth=1)
    # plt.plot(t_vals, gyro_z, label='z-gyro', linewidth=1)
    # plt.ylim([-20, 20])
    # plt.xlabel("Test time (seconds)")
    # plt.ylabel("Angular Velocity (degrees/second$)")

    # plt.plot(t_vals, mag_x, label='x-mag', linewidth=1)
    # plt.plot(t_vals, mag_y, label='y-mag', linewidth=1)
    # plt.plot(t_vals, mag_z, label='z-mag', linewidth=1)
    # plt.ylim([-20, 20])
    # plt.xlabel("Test time (seconds)")
    # plt.ylabel("Magnetic flux")

    # plt.plot(t_vals, q0, label='q0', linewidth=1)
    # plt.plot(t_vals, q1, label='q1', linewidth=1)
    # plt.plot(t_vals, q2, label='q2', linewidth=1)
    # plt.plot(t_vals, q3, label='q3', linewidth=1)
    # plt.ylim([-1.5, 1.5])
    # plt.xlabel("Test time (seconds)")
    # plt.ylabel("Quaternion magnitude)")

    plt.plot(t_vals, d0, label='d0', linewidth=1)
    plt.plot(t_vals, d1, label='d1', linewidth=1)
    plt.plot(t_vals, d2, label='d2', linewidth=1)
    plt.ylim([-180, 180])
    plt.xlabel("Test time (seconds)")
    plt.ylabel("Degrees)")


    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.grid(True)
    if t_curr >= 15:
        plt.xlim(t_curr - 15, t_curr + 5)
    else:
        plt.xlim(0, 20)



ani = FuncAnimation(plt.gcf(), animate, interval=50)

plt.tight_layout()
plt.show()
