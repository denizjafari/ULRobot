import csv
import time
import math
from python import osc_decoder
import socket
import numpy as np
from ahrs import Quaternion
from ahrs.filters import Mahony

# Send /identify message to strobe all LEDs.  The OSC message is constructed
# from raw bytes as per the OSC specification.  The IP address must be equal to
# the IP address of the target NGIMU.

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.sendto(bytes("/identify\0\0\0,\0\0\0", "utf-8"), ("192.168.2.219", 9000))
send_socket.sendto(bytes("/unmute\0\0\0\0\0,\0\0\0", "utf-8"), ("192.168.45.9", 9000))

# Array of UDP ports to listen to, one per NGIMU.  These ports must be equal to
# the UDP Send Port in the NGIMU settings.  The UDP Send IP Address setting
# must be the computer's IP address.  Both these settings are changed
# automatically when connecting to the NGIMU using the NGIMU GUI.
receive_ports = [8009]
receive_sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(len(receive_ports))]

index = 0
for receive_socket in receive_sockets:
    receive_socket.bind(("", receive_ports[index]))
    index = index + 1
    receive_socket.setblocking(False)


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


def write_to_csv(readings):
    with (open('data/data.csv', 'a') as csv_file):
        names = ["Time_Stamp", "ACCEL_LN_X", "ACCEL_LN_Y", "ACCEL_LN_Z", "GYRO_X", "GYRO_Y", "GYRO_Z", "MAG_X",
                 "MAG_Y", "MAG_Z", "EMG_1", "EMG_2", "q0", "q1", "q2", "q3", "d0", "d1", "d2", "d'0", "d'1", "d'2"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=names)

        acc = np.ndarray(shape=(1, 3), dtype=float,
                         buffer=np.array([readings[3] * 9.81, readings[4] * 9.81, readings[5] * 9.81]))
        gyro = np.ndarray(shape=(1, 3), dtype=float, buffer=np.array([readings[0], readings[1], readings[2]]))
        mag = np.ndarray(shape=(1, 3), dtype=float, buffer=np.array([readings[6], readings[7], readings[8]]))
        orientation1 = Mahony(gyr=gyro, acc=acc, mag=mag)  # Calculate orientation from ahrs module

        Q = Quaternion(orientation1.Q[0])  # Save quaternion vector
        Q2 = readings[9:12]
        degrees = [x * 180 / math.pi for x in (Q2.to_angles())]  # Calculate Euler angles from Xio quaternions
        degrees2 = [x * 180 / math.pi for x in (Q.to_angles())]  # Calculate Euler angles from ahrs quaternions

        info = {
            "Time_Stamp": time.time() - now,
            "ACCEL_LN_X": readings[3] * 9.81,
            "ACCEL_LN_Y": readings[4] * 9.81,
            "ACCEL_LN_Z": readings[5] * 9.81,
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
            "d0": degrees[0],
            "d1": degrees[1],
            "d2": degrees[2],
            "d'0": degrees2[0],
            "d'1": degrees2[1],
            "d'2": degrees2[2],

        }
        csv_writer.writerow(info)


name_csv()
now = time.time()

while True:
    for udp_socket in receive_sockets:
        try:
            data, addr = udp_socket.recvfrom(2048)
        except socket.error:
            pass
        else:
            for message in osc_decoder.decode(data):
                if message[1] == '/sensors':
                    # print(message[2:11])
                    data = message[2:11]
                if message[1] == '/quaternion':
                    # print(message[2:6])
                    data.extend(message[2:6])
                    # print(data)
                    write_to_csv(data)
