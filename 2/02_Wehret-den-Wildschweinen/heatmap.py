#!/usr/bin/env python3
from _decimal import Decimal, ROUND_UP

import numpy as np
import matplotlib.pylab as plt
from matplotlib import colors
import os


def round(x):
    return float(Decimal(str(x)).quantize(Decimal('.001'), rounding=ROUND_UP))


def visualize(path):
    matrix = np.loadtxt(path, skiprows=1)
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.get_cmap('hot'))
    plt.colorbar()
    plt.show()


def possible_paths(n):
    path = "res/wildschwein{}.txt".format(n)
    matrix = np.loadtxt(path, skiprows=1)

    N = len(matrix)

    # top -> bot
    top_to_bot_float = np.matrix([[0.0] * N] * N)
    top_to_bot_bool = np.matrix([[True] * N] * N)
    # bot -> top
    bot_to_top_float = np.matrix([[0.0] * N] * N)
    bot_to_top_bool = np.matrix([[True] * N] * N)
    # left -> right
    left_to_right_float = np.matrix([[0.0] * N] * N)
    left_to_right_bool = np.matrix([[True] * N] * N)
    # right -> left
    right_to_left_float = np.matrix([[0.0] * N] * N)
    right_to_left_bool = np.matrix([[True] * N] * N)

    for i in range(N):
        for j in range(N):
            # top -> bot
            if i != N - 1:
                top_to_bot_float[i, j] = abs(matrix[i, j] - matrix[i+1, j])
                top_to_bot_bool[i, j] = abs(matrix[i, j] - matrix[i+1, j]) < 1
            # bot -> top
            if i != 0:
                bot_to_top_float[i, j] = abs(matrix[i, j] - matrix[i-1, j])
                bot_to_top_bool[i, j] = abs(matrix[i, j] - matrix[i-1, j]) < 1
            # left -> right
            if j != N - 1:
                left_to_right_float[i, j] = abs(matrix[i, j] - matrix[i, j+1])
                left_to_right_bool[i, j] = abs(matrix[i, j] - matrix[i, j+1]) < 1
            # right -> left
            if j != 0:
                right_to_left_float[i, j] = abs(matrix[i, j] - matrix[i, j-1])
                right_to_left_bool[i, j] = abs(matrix[i, j] - matrix[i, j-1]) < 1

    try:
        os.mkdir("out")
    except FileExistsError:
        print("out/ already exists")

    try:
        os.mkdir("out/wildschwein{}".format(n))
    except FileExistsError:
        print("out/wildschwein{} already exists".format(n))

    # overview
    plt.imshow(matrix, interpolation='nearest', cmap='hot')
    plt.savefig("out/wildschwein{}/heatmap.png".format(n), bbox_inches='tight')

    # bool
    # top -> bot
    plt.imshow(top_to_bot_bool, interpolation='nearest', cmap='Greys_r', vmin=0, vmax=1)
    plt.savefig("out/wildschwein{}/top_to_bot_bool.png".format(n), bbox_inches='tight')

    # bot -> top
    plt.imshow(bot_to_top_bool, interpolation='nearest', cmap='Greys_r', vmin=0, vmax=1)
    plt.savefig("out/wildschwein{}/bot_to_top_bool.png".format(n), bbox_inches='tight')

    # left -> right
    plt.imshow(left_to_right_bool, interpolation='nearest', cmap='Greys_r', vmin=0, vmax=1)
    plt.savefig("out/wildschwein{}/left_to_right_bool.png".format(n), bbox_inches='tight')

    # right -> left
    plt.imshow(right_to_left_bool, interpolation='nearest', cmap='Greys_r', vmin=0, vmax=1)
    plt.savefig("out/wildschwein{}/right_to_left_bool.png".format(n), bbox_inches='tight')

    # float
    # top -> bot
    plt.imshow(top_to_bot_float, interpolation='nearest', cmap='hot')
    plt.colorbar()
    plt.savefig("out/wildschwein{}/top_to_bot_float.png".format(n), bbox_inches='tight')

    # bot -> top
    plt.imshow(bot_to_top_float, interpolation='nearest', cmap='hot')
    plt.savefig("out/wildschwein{}/bot_to_top_float.png".format(n), bbox_inches='tight')

    # left -> right
    plt.imshow(left_to_right_float, interpolation='nearest', cmap='hot')
    plt.savefig("out/wildschwein{}/left_to_right_float.png".format(n), bbox_inches='tight')

    # right -> left
    plt.imshow(right_to_left_float, interpolation='nearest', cmap='hot')
    plt.savefig("out/wildschwein{}/right_to_left_float.png".format(n), bbox_inches='tight')

if __name__ == '__main__':
    possible_paths(5)