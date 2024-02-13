import math
import matplotlib.pyplot as plt
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
