import numpy as np
import time
from math import log, exp

"""
pseudo-random number generators
"""


# linear congruential generator
# n = amount of numbers to return
def linear_congruential_generator(seed=int(time.clock() * pow(10, 20)), n=1):
    x0 = seed
    a = 1103515245
    c = 12345
    M = 34843546

    random = []
    last_x = x0

    for i in range(n):
        x = (a * last_x + c) % M
        last_x = x
        U = float(x / M)

        random.append(U)

    return random


def exponential_generator(seed=int(time.clock() * pow(10, 20)), n=1):
    x0 = seed
    a = 1103515245
    c = 12345
    M = 34843546
    lambd = 8

    random = []
    last_x = x0

    for i in range(n):
        x = (a * last_x + c) % M
        last_x = x
        U = float(x / M)
        U = (-1 / lambd) * log(U)

        random.append(U)

    return random


def poisson_generator(lambd=50, n=1):
    random = []

    for i in range(n):
        x = 0
        p = 1

        while p >= exp(-lambd):
            i = np.random.random()
            p = p * i
            x += 0.01

        random.append(x)

    return random


for i in range(10):
    print(exponential_generator(time.clock() * pow(10, 20))[0] * 100)
