import matplotlib.pyplot as plt
import os.path
from datetime import date, datetime
import csv
import math
import numpy as np


def rnd(num):
    if -1 <= num <= 1:
        num = 0
    return np.round(num, 3)


def newtons(kilos, g):
    return kilos * g


def deg2rad(deg):
    return deg * np.pi / 180


def rad2deg(rad):
    return rad * 180 / np.pi


def lb2n(lbs):
    return lbs * 4.4482189159


def lb2kg(lbs):
    return lbs * 0.453592


def kg2lb(kgs):
    return kgs / 0.453592


def normalise_arrays(x, y, z):
    if len(x) != len(y) != len(z):
        print("Error, lists are not equal length")
    else:
        magnitude = np.zeros(len(x))
        for i in range(len(x)):
            magnitude[i] = math.sqrt(x[i] ** 2 + y[i] ** 2 + z[i] ** 2)
        return magnitude


# to allocate :  IMU1 = Sensor(name, channel, data_outputs)
# to pull data:  IMU1.name , IMU1.channels
def check_active_channels(current_device):  # Checks and assigns sensor data outputs
    active_channels = current_device.get_data_types()
    channels = ""

    if 'EChannelType.ACCEL_LN_X' in str(active_channels):
        channels = channels + "A"

    if 'EChannelType.GYRO_MPU9150_Y' in str(active_channels):
        channels = channels + "G"

    if 'EChannelType.MAG_LSM303DLHC_X' in str(active_channels):
        channels = channels + "M"
    else:
        print("Something is wrong, your device lacks IMU Shimmer channels...")
    if 'EChannelType.EXG_ADS1292R_1_CH1_24BIT' in str(active_channels):
        channels = channels + "E"
    else:
        print("No ECG/EMG detected!")
    return channels


def get_calibration_data(name):
    print("Calibration check: sensor " + name)
    filename = str("calib_data/" + name + ".ini")

    if os.path.exists(filename):  # Checks to see if calibration file exists for the given sensor
        B = np.array(np.zeros((3, 3)))  # Generate empty offset matrix
        K = np.array(np.zeros((3, 3)))  # Generate empty sensitivity matrix
        R = np.array(np.zeros((3, 9)))  # Generate empty orientation matrix
        calib_data = np.array([])  # Generate calibration data array
        data = open("calib_data/" + name + ".ini",
                    "r")  # Open ini calibration file. Must be named the same as the called device!

        for line in data:
            line = line.strip('\n')
            line = line.split("= ")
            if len(line) > 1:
                calib_data = np.append(calib_data, line[1])

        # Fill matrices with data
        B[0, :] = calib_data[0:3]
        B[1, :] = calib_data[15:18]
        B[2, :] = calib_data[30:33]
        K[0, :] = calib_data[3:6]
        K[1, :] = calib_data[18:21]
        K[2, :] = calib_data[33:36]
        R[0, :] = calib_data[6:15]
        R[1, :] = calib_data[21:30]
        R[2, :] = calib_data[36:45]
        print("Calibration record found! Applying...")
    else:
        B = np.array([[2047, 2047, 2047], [0, 0, 0], [0, 0, 0]])  # Assign default offset matrix
        K = np.array([[83, 83, 83], [65.5, 65.5, 65.5], [1100, 110, 980]])  # Assign default sensitivity matrix
        R = np.array([[0, -1, 0, -1, 0, 0, 0, 0, -1], [0, -1, 0, -1, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 1, 0, 0, 0, -1]])
        print("NO CALIBRATION DATA... default values applied...")

    print("Offset matrix, sensor " + name + " =")
    print(B)
    print("Sensitivity matrix, sensor " + name + " =")
    print(K)
    print("Orientation matrix, sensor " + name + " =")
    print(R)
    return B, K, R, name


def name_csv():
    names = ["Time_Stamp", "ACCEL_LN_X", "ACCEL_LN_Y", "ACCEL_LN_Z", "GYRO_X", "GYRO_Y", "GYRO_Z", "MAG_X", "MAG_Y",
             "MAG_Z", "EMG_1", "EMG_2", "q0", "q1", "q2", "q3", "d0", "d1", "d2"]
    units = ["s", "m/s^2", "m/s^2", "m/s^2", "deg/s", "deg/s", "deg/s", "localFlux", "localFlux", "localFlux", "mV",
             "mV", 'scalar', 'i', 'j', 'k', 'deg', 'deg', 'deg']

    today = date.today()
    # filename = "data/" + str(today) + "_" + time_filename + name + ".csv"
    filename = "data/data.csv"  # Test override!!!
    with open(filename, 'w') as csv_file:  # THis part writes headers into the CSV file
        csv_writer_names = csv.DictWriter(csv_file, fieldnames=names)
        csv_writer_names.writeheader()
        csv_writer_units = csv.DictWriter(csv_file, fieldnames=units)
        csv_writer_units.writeheader()
    return filename

def makeplot(x, y, labels, legend):
    plt.style.use('classic')
    fig, ax = plt.subplots()

    if y.size == len(y):
        ax.plot(x, y)
        limits = [min(y) * 0.9, max(y) * 1.1]

    else:
        for i in range(len(y[1])):
            ax.plot(x, y[:, i])

        limits = [min(min(row) for row in y) * 0.9, max(max(row) for row in y) * 1.1]

    ax.set(xlabel=labels[0], ylabel=labels[1],
           title=labels[2])

    plt.ylim(limits)
    ax.grid()
    plt.legend(legend, loc="lower right", fontsize='small')
    fig.savefig(labels[3], dpi=500)


def normalise_array(arr):
    total = 0
    for i in range(len(arr)):
        total = arr[i] * arr[i]
    return math.sqrt(total)


def normalise_arrays(x, y, z):
    if len(x) != len(y) != len(z):
        print("Error, lists are not equal length")
    else:
        magnitude = np.zeros(len(x))
        for i in range(len(x)):
            magnitude[i] = math.sqrt(x[i] ** 2 + y[i] ** 2 + z[i] ** 2)
        return magnitude
