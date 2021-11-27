# -*- coding: utf-8 -*-
"""

"""

# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import levy
import matplotlib.pyplot as plt

from matplotlib import animation
from IPython.display import HTML


class FPA():
    def __init__(self, switch_probability=0.8, n_flowers=50, n_parameters=2, constraints=None):
        # Initialization of variables
        self.sp = switch_probability
        self.n_flowers = n_flowers
        self.flowers = [None]*n_flowers
        self.cost = np.zeros(n_flowers)
        self.random = np.random
        self.n_parameters = n_parameters
        self.const = constraints

        # Random Initial Flowers
        self.init_flowers()
        # Get the best flower from initial population
        self.best = self.flowers[self.cost.argmin()]

    # This is the objective function, modify this according to your needs.
    def Six_Hump_Camel(self, x):
        output = (4 - 2.1*(x[0]**2) + (x[0]**4)/3) * \
            x[0]**2 + x[0] * x[1] + (-4 + 4*x[1]**2) * x[1]**2
        return output

    def global_pollination(self, x):  # Global pollination
        x_new = x + levy.rvs(size=x.shape[0]) * (self.best - x)
        return x_new

    def local_pollination(self, x, x1, x2):  # Local Pollination
        x_new = x + self.random.randn() * (x1 - x2)
        return x_new

    def init_flowers(self):  # Initialization of flowers
        for i in range(self.n_flowers):
            self.flowers[i] = self.random.rand(self.n_parameters)
            for j in range(self.n_parameters):
                if self.const is not None:
                    self.flowers[i][j] = self.flowers[i][j] * \
                        (self.const[j][1] - self.const[j][0]) + \
                        self.const[j][0]
                else:
                    self.flowers[i][j] = self.flowers[i][j] * 100 - 50
            self.cost[i] = self.Six_Hump_Camel(self.flowers[i])

    def optimize(self, max_gen=100):
        # Save history for plotting
        history = np.zeros((max_gen, self.n_parameters))

        # Generation loop
        for i in range(max_gen):
            history[i, :] = self.best  # Update history

            # Flower loop
            for j in range(self.n_flowers):
                p = self.random.rand()

                # Global Pollination if p <= switch probability
                if p <= self.sp:
                    x_temp = self.global_pollination(self.flowers[j])

                # Local Pollination if p > switch probability
                else:
                    r1 = self.random.randint(0, high=self.n_flowers)
                    r2 = self.random.randint(0, high=self.n_flowers)
                    while r2 == r1:
                        r2 = self.random.randint(0, high=self.n_flowers)
                    x_temp = self.local_pollination(
                        self.flowers[j], self.flowers[r1], self.flowers[r2])

                # Apply constraints
                if self.const is not None:
                    for k in range(self.n_parameters):
                        x_temp = np.clip(
                            x_temp, self.const[k][0], self.const[k][1])
                else:
                    continue

                # Calculate cost
                cost_temp = self.Six_Hump_Camel(x_temp)

                # Compare the newly generated flower with the previous flower
                if cost_temp < self.cost[j]:
                    self.flowers[j] = x_temp
                    self.cost[j] = cost_temp
                else:
                    continue

            # Update best
            self.best = self.flowers[self.cost.argmin()]

        return self.flowers, self.cost, history


const = [np.array([-2.5, 2.5]), np.array([-1.5, 1.5])]
FPA = FPA(switch_probability=0.6, n_flowers=5,
          n_parameters=2, constraints=const)
result, cost, hist = FPA.optimize(25)


print(result[cost.argmin()])
