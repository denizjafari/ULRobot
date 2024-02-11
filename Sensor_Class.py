import math

import numpy as np
import os.path
from pyshimmer import ShimmerBluetooth, DEFAULT_BAUDRATE, DataPacket, EChannelType, ChannelDataType, reader
from datetime import date, datetime
import csv
import time


class Sensor:
    count = 0
    start = 0
    stream_names = ["Time_Stamp", "ACCEL_LN_X", "ACCEL_LN_Y", "ACCEL_LN_Z", "GYRO_X", "GYRO_Y", "GYRO_Z", "MAG_X",
                    "MAG_Y",
                    "MAG_Z", "EMG_1", "EMG_2", "q0", "q1", "q2", "q3", "d0", "d1", "d2"]
    # Default offset matrix
    Ba = np.array([2047, 2047, 2047], dtype=np.float64)
    Bg = np.array([0, 0, 0], dtype=np.float64)
    Bm = np.array([0, 0, 0], dtype=np.float64)

    Ka = np.array([[83, 0, 0], [0, 83, 0], [0, 0, 83]], dtype=np.float64)
    Kg = np.array([[131, 0, 0], [0, 131, 0], [0, 0, 131]], dtype=np.float64)
    Km = np.array([[1100, 0, 0], [0, 1100, 0], [0, 0, 980]], dtype=np.float64)

    Ra = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=np.float64)
    Rg = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=np.float64)
    Rm = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=np.float64)

    sampling_rate = 0  # Placeholder
    data_channels = [
        ["Time_Stamp", "ACCEL_LN_X", "ACCEL_LN_Y", "ACCEL_LN_Z", "GYRO_X", "GYRO_Y", "GYRO_Z", "MAG_X",
         "MAG_Y",
         "MAG_Z", "q0", "q1", "q2", "q3", "d0", "d1", "d2"]]
    units = ["s", "m/s^2", "m/s^2", "m/s^2", "deg/s", "deg/s", "deg/s", "localFlux", "localFlux", "localFlux", 'scalar',
             'i', 'j', 'k', 'deg', 'deg', 'deg']
    has_EMG = False
    acc = [0, 0, 0]
    gyro = [0, 0, 0]
    mag = [0, 0, 0]
    emg = [0, 0]

    quat = [0, 0, 0, 0]

    def __init__(self, name, port):
        Sensor.count += 1
        self.name = name  # Name of device here
        self.port = '/dev/' + port  # Comm port name
        self.filename = "data/data.csv"

    def process_raw_data(self):
        self.acc = np.array(np.matmul(np.matmul(np.linalg.inv(self.Ra), np.linalg.inv(self.Ka)),
                                       np.transpose(self.acc - self.Ba)))
        #
        self.gyro = np.transpose(np.array(np.matmul(np.matmul(np.linalg.inv(self.Rg), np.linalg.inv(self.Kg)),
                                                    np.transpose(self.gyro - self.Bg))))

        self.mag = np.transpose(np.array(np.matmul(np.matmul(np.linalg.inv(self.Rm), np.linalg.inv(self.Km)),
                                                   np.transpose(self.mag - self.Bm))))

    # # self.data_outputs = data_outputs
    # def handler(self, pkt: DataPacket) -> None:
    #     for i in range(Sensor.count):
    #         with (open(self[i].filename, 'a') as csv_file):
    #             Sensor.time[1] = time.time() - Sensor.time[0]  #
    #
    #             IMU[i].acc = (
    #                 [pkt[EChannelType.ACCEL_LN_X], pkt[EChannelType.ACCEL_LN_X], pkt[EChannelType.ACCEL_LN_X]])
    #             IMU[i].gyro = (
    #                 [pkt[EChannelType.GYRO_MPU9150_X] * math.pi / 180, pkt[EChannelType.GYRO_MPU9150_Y] * math.pi / 180,
    #                  pkt[EChannelType.GYRO_MPU9150_Z] * math.pi / 180])
    #             IMU[i].mag = ([pkt[EChannelType.MAG_LSM303DLHC_X], pkt[EChannelType.MAG_LSM303DLHC_Y],
    #                            pkt[EChannelType.MAG_LSM303DLHC_Z]])
    #
    #             if IMU[i].has_EMG == True:
    #                 IMU[i].emg = (
    #                     [pkt[EChannelType.EXG_ADS1292R_1_CH1_24BIT], pkt[EChannelType.EXG_ADS1292R_2_CH2_24BIT]])

    def get_calibration(self):  # Checks for calibration file in the sensor_data directory.
        # If unavailable, leaves default values assigned to the sensor
        print('\n')
        print("Calibration check: sensor " + self.name)
        filename = str("sensor_data/" + self.name + ".ini")

        if os.path.exists(filename):  # Checks to see if calibration file exists for the given sensor
            calib_data = np.array([])  # Generate calibration data array
            data = open("calib_data/" + self.name + ".ini",
                        "r")  # Open ini calibration file. Must be named the same as the called device!

            for line in data:
                line = line.strip('\n')
                line = line.split("= ")
                if len(line) > 1:
                    calib_data = np.append(calib_data, line[1])

            # Fill matrices with data
            self.Ba = np.array([calib_data[0], calib_data[1], calib_data[2]], dtype=np.float64)
            self.Bg = np.array([calib_data[15], calib_data[16], calib_data[17]], dtype=np.float64)
            self.Bm = np.array([calib_data[30], calib_data[31], calib_data[32]], dtype=np.float64)

            self.Ka = np.array([[calib_data[3], 0, 0], [0, calib_data[4], 0], [0, 0, calib_data[5]]], dtype=np.float64)
            self.Kg = np.array([[calib_data[18], 0, 0], [0, calib_data[19], 0], [0, 0, calib_data[20]]],
                               dtype=np.float64)
            self.Km = np.array([[calib_data[33], 0, 0], [0, calib_data[34], 0], [0, 0, calib_data[35]]],
                               dtype=np.float64)

            self.Ra = np.array([calib_data[6:9], calib_data[9:12], calib_data[12:15]], dtype=np.float64)
            self.Rg = np.array([calib_data[21:24], calib_data[24:27], calib_data[27:30]], dtype=np.float64)
            self.Rm = np.array([calib_data[36:39], calib_data[39:42], calib_data[42:45]], dtype=np.float64)

            print("Calibration record found! Applying...")

        else:
            print("No calibration data found, applying default values...")
        self.print_calibration_matrices()

    def print_calibration_matrices(self):
        print("Acceleration calibration matrices, sensor " + self.name + " =")
        print(self.Ba)
        print(self.Ka)
        print(self.Ra)
        print("Gyroscope calibration matrices, sensor " + self.name + " =")
        print(self.Bg)
        print(self.Kg)
        print(self.Rg)
        print("Magnetometer calibration matrices, sensor " + self.name + " =")
        print(self.Bm)
        print(self.Km)
        print(self.Rm)
        print('\n')


def name_csv(self, filename):
    if self.has_EMG == True:
        self.data_channels.append(["EMG_1", "EMG_2"])
        self.units.append(["mV", "mV"])
    # today = date.today()
    # filename = "data/" + str(today) + "_" + time_filename + name + ".csv"
    with open(filename, 'w') as csv_file:  # THis part writes headers into the CSV file
        csv_writer_names = csv.DictWriter(csv_file, fieldnames=self.data_channels)
        csv_writer_names.writeheader()
        csv_writer_units = csv.DictWriter(csv_file, fieldnames=self.units)
        csv_writer_units.writeheader()


def load_sensors():  # Load sensor comm ports and names from text file
    filename = "sensor_data/Sensors.txt"
    ID = []
    Name = []
    if os.path.exists(filename):
        sensors = open(filename, "r")
        for line in sensors:
            sensor_info = line.split(", ")
            sensor_name = (sensor_info[1])
            sensor_name = sensor_name.split("\n")
            ID.append("/dev/" + str(sensor_info[0]))
            Name.append(sensor_name[0])
        return ID, Name
    else:
        print("Error. No text file with sensor information was found.")


if __name__ == '__main__':
    IMU = []
    Ports, Names = load_sensors()
    for i in range(len(Names)):
        IMU.append(Sensor(Names[i], Ports[i]))
    print('\n')
    print("%d sensors identified." % len(IMU))
    print(IMU[1].filename)
    print(IMU[0].filename)
    print(Sensor.count)
