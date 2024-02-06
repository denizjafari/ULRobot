# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import csv
import logging
import numpy as np
import sys
import time

from Adafruit_BNO055 import BNO055

prev_millis = 0
sampling = 20  # Magnetometer sampling at 20hz, everything else, 100hz.

# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
# BeagleBone Black configuration with default I2C connection (SCL=P9_19, SDA=P9_20),
# and RST connected to pin P9_12:
# bno = BNO055.BNO055(rst='P9_12')


# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')


def check_time():
    global prev_millis
    time_millis = 1000 * (time.time() - start)
    if time_millis >= (1000 / sampling) + prev_millis:
        prev_millis = time_millis
        write_to_csv()


def get_data():
    data = np.zeros(12)
    data[10], data[11], data[12], data[9] = bno.read_quaterion()
    data[6], data[7], data[8] = bno.read_magnetometer()
    data[0], data[1], data[2] = bno.read_gyroscope()
    data[3], data[4], data[5] = bno.read_accelerometer()
    return data


def name_csv():
    names = ["Time_Stamp", "ACCEL_LN_X", "ACCEL_LN_Y", "ACCEL_LN_Z", "GYRO_X", "GYRO_Y", "GYRO_Z", "MAG_X",
             "MAG_Y", "MAG_Z", "EMG_1", "EMG_2", "q0", "q1", "q2", "q3", "d0", "d1", "d2", "d'0", "d'1", "d'2"]
    units = ["s", "m/s^2", "m/s^2", "m/s^2", "deg/s", "deg/s", "deg/s", "localFlux", "localFlux", "localFlux", 'mV',
             'mV',
             'scalar',
             'i', 'j', 'k', 'deg', 'deg', 'deg', 'deg', 'deg', 'deg']
    # today = date.today()
    # filename = "data/" + str(today) + "_" + time_filename + name + ".csv"
    with open('data/data.csv', 'w') as csv_file:  # THis part writes headers into the CSV file
        csv_writer_names = csv.DictWriter(csv_file, fieldnames=names)
        csv_writer_names.writeheader()
        csv_writer_units = csv.DictWriter(csv_file, fieldnames=units)
        csv_writer_units.writeheader()


def write_to_csv():
    with (open('data/data.csv', 'a') as csv_file):
        names = ["Time_Stamp", "ACCEL_LN_X", "ACCEL_LN_Y", "ACCEL_LN_Z", "GYRO_X", "GYRO_Y", "GYRO_Z", "MAG_X",
                 "MAG_Y", "MAG_Z", "EMG_1", "EMG_2", "q0", "q1", "q2", "q3", "d0", "d1", "d2", "d'0", "d'1", "d'2"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=names)

        readings = get_data()

        info = {
            "Time_Stamp": time.time() - start,
            "ACCEL_LN_X": readings[3],
            "ACCEL_LN_Y": readings[4],
            "ACCEL_LN_Z": readings[5],
            "GYRO_X": readings[0],
            "GYRO_Y": readings[1],
            "GYRO_Z": readings[2],
            "MAG_X": readings[6],
            "MAG_Y": readings[7],
            "MAG_Z": readings[8],
            "EMG_1": 0,
            "EMG_2": 0,
            "q0": readings[9],
            "q1": readings[10],
            "q2": readings[11],
            "q3": readings[12],
            "d0": 0,
            "d1": 0,
            "d2": 0,
            "d'0": 0,
            "d'1": 0,
            "d'2": 0,

        }
        csv_writer.writerow(info)


name_csv()
start = time.time()


while True:
    check_time()
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
        heading, roll, pitch, sys, gyro, accel, mag))
    # Other values you can optionally read:
    # Orientation as a quaternion:
    # x,y,z,w = bno.read_quaterion()
    # Sensor temperature in degrees Celsius:
    # temp_c = bno.read_temp()
    # Magnetometer data (in micro-Teslas):
    # x,y,z = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    # x, y, z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    # x,y,z = bno.read_accelerometer()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    # x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    # x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.
