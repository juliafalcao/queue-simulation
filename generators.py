import numpy as np
import time
from math import log, exp
import matplotlib.pyplot as plt

"""
pseudo-random number generators
ps.: seed is mandatory, pass time.time() when calling functions
"""

# linear congruential generator
# returns one random generated number
def linear_congruential_generator(seed, a = 1103515245, c = 12345, M = 34843546):
    x0 = seed
    
    x = (a * x0 + c) % M
    U = float(x / M)

    return U

def exponential_generator(seed, lambd = 8):
    U = linear_congruential_generator(seed)
    U = (-1 / lambd) * log(U)

    return U


random = []

for i in range(999999):
    random.append(exponential_generator(seed = np.random.randint(0, 9999999999999)))

plt.hist(random, rwidth = 0.5)
plt.show()

def poisson_generator(seed, lambd = 50):
    x = 0
    p = 1

    while p >= exp(-lambd):
        i = np.random.random()
        p = p * i
        x += 0.01

    return x