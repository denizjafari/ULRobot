from ahrs.filters import Mahony
from python.Sensor_Class import *
import functions
from ahrs import Quaternion
import math
import time
import numpy as np
from serial import Serial
from datetime import datetime
from pyshimmer import ShimmerBluetooth, DEFAULT_BAUDRATE, DataPacket, EChannelType
import csv


def get_data(pkt):  # Collect data from data packets and save to sensor class
    IMU1.acc[0] = pkt[EChannelType.ACCEL_LN_X]
    IMU1.acc[1] = pkt[EChannelType.ACCEL_LN_Y]
    IMU1.acc[2] = pkt[EChannelType.ACCEL_LN_Z]
    IMU1.gyro[0] = pkt[EChannelType.GYRO_MPU9150_X] * math.pi / 180
    IMU1.gyro[1] = pkt[EChannelType.GYRO_MPU9150_Y] * math.pi / 180
    IMU1.gyro[2] = pkt[EChannelType.GYRO_MPU9150_Z] * math.pi / 180
    IMU1.mag[0] = pkt[EChannelType.MAG_LSM303DLHC_X]
    IMU1.mag[1] = pkt[EChannelType.MAG_LSM303DLHC_Y]
    IMU1.mag[2] = pkt[EChannelType.MAG_LSM303DLHC_Z]
    if IMU1.has_EMG:
        IMU1.emg[0] = pkt[EChannelType.EXG_ADS1292R_1_CH1_24BIT]
        IMU1.emg[1] = pkt[EChannelType.EXG_ADS1292R_1_CH2_24BIT]
    IMU1.process_raw_data()  # Calculate output data from raw data and calibration information


def handler(pkt: DataPacket) -> None:
    with (open(IMU1.filename, 'a') as csv_file):
        get_data(pkt)  # Gets the data from the data packet
        csv_writer = csv.DictWriter(csv_file, fieldnames=IMU1.stream_names)
        acc = np.ndarray(shape=(1, 3), dtype=float, buffer=np.array(IMU1.acc))
        gyro = np.ndarray(shape=(1, 3), dtype=float, buffer=np.array(IMU1.gyro))
        mag = np.ndarray(shape=(1, 3), dtype=float, buffer=np.array(IMU1.mag))
        orientation1 = Mahony(gyr=gyro, acc=acc, mag=mag)  # Calculate orientation from ahrs module
        Q = Quaternion(orientation1.Q[0])  # Save quaternion vector
        degrees = [x * 180 / math.pi for x in (Q.to_angles())]  # Calculate Euler angles
        info = {
            "Time_Stamp": time.time() - Sensor.start,
            "ACCEL_LN_X": IMU1.acc[0],
            "ACCEL_LN_Y": IMU1.acc[1],
            "ACCEL_LN_Z": IMU1.acc[2],
            "GYRO_X": IMU1.gyro[0],
            "GYRO_Y": IMU1.gyro[1],
            "GYRO_Z": IMU1.gyro[2],
            "MAG_X": IMU1.mag[0],
            "MAG_Y": IMU1.mag[1],
            "MAG_Z": IMU1.mag[2],
            "EMG_1": IMU1.emg[0],
            "EMG_2": IMU1.emg[1],
            "q0": Q[0],
            "q1": Q[1],
            "q2": Q[2],
            "q3": Q[3],
            "d0": degrees[0],
            "d1": degrees[1],
            "d2": degrees[2],

        }
        csv_writer.writerow(info)  # Write to csv


if __name__ == '__main__':
    IMU1 = Sensor('95A7', 'rfcomm1')  # Define sensor IMU1 with name and com port
    IMU1.get_calibration()  # Check file directory for calibration file
    functions.name_csv()  # Name csv file
    now = datetime.now()  # Start time of main script for csv filename
    time_current = now.strftime("%H-%M-%S_")  # Start time of main script for csv filename

    # IMU1.filename = functions.name_csv(IMU1.name,
    #                                time_current)  # Create timestamped and named csv file and return the filename

    serial = Serial(IMU1.port, DEFAULT_BAUDRATE)  # Define serial info and connect (from PyShimmer module)
    shim_dev = ShimmerBluetooth(serial)
    shim_dev.initialize()  # Connect and initialise communications

    Sensor.start = time.time()  # Define start time
    shim_dev.add_stream_callback(handler)  # Commence data transfer
    shim_dev.start_streaming()

    time.sleep(600.0)  # Stop time and stop sequence
    shim_dev.stop_streaming()
    shim_dev.shutdown()
