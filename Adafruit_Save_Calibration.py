import csv
import numpy as np
import board
import adafruit_bno055

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_bno055.BNO055_I2C(i2c)
# If you are going to use UART uncomment these lines
# uart = board.UART()
# sensor = adafruit_bno055.BNO055_UART(uart)
last_val = 0xFFFF


acc = [0, 0, 0]
gyro = mag = acc
acc_not_set = True
gyro_not_set = True
mag_not_set = True


def enter_parameters(set, status, label):
    while status:
        for i in range(3):
            set[i] = int(input("Enter {name} offset {iteration} \n".format(name=label, iteration=i + 1)))
        print(set)
        string = input("Is this correct? y/n \n")
        if string == 'y':
            status = False
            set = tuple(set)
            return set
        else:
            pass



while True:
    print("Current Settings: \n", sensor.offsets_accelerometer, sensor.offsets_gyroscope, sensor.offsets_magnetometer)

    acc = enter_parameters(acc, acc_not_set, "acceleration")
    gyro = enter_parameters(gyro, gyro_not_set, "gyroscope")
    mag = enter_parameters(mag, mag_not_set, "magnetometer")

    print("Saving accelerometer values...")
    sensor.offsets_accelerometer = acc
    if sensor.offsets_accelerometer == acc:
        print("Accelerometer offset updated")
    else:
        print("Failed")

    print("Saving gyroscope values...")
    sensor.offsets_gyroscope = gyro
    if sensor.offsets_gyroscope == gyro:
        print("Gyroscope offset updated")
    else:
        print("Failed")

    print("Saving magnetometer values...")
    sensor.offsets_magnetometer = mag
    if sensor.offsets_magnetometer == mag:
        print("Magnetometer offset updated")
    else:
        print("Failed")

    break


