import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def relu(x):
    if x > 0:
        return x
    else:
        return 0


def leaky_relu(x):
    if x > 0:
        return x
    else:
        return 0.01 * x


def tanh(x):
    return 2 / (1 + np.exp(-2 * x))
