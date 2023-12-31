'''
reset method of the environment
Reset the environment after 'done'
'''
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np

def allocation_amount(num_people, amount): #return a random list of num_people in length and amount in sum.
    a = [np.random.randint(0, amount) for i in range(num_people-1)]
    a.append(0)
    a.append(amount)
    a.sort()
    print(a)
    b = [a[i+1]-a[i] for i in range(num_people)]
    print(b)
    b = np.array(b)
    return b

def reset(self, seed=None, options=None):
    super(type(self), self).reset(seed=seed)

    # sample agent and target locations
    # The agent always starts at the center of the board
    self.agent_location = np.array([int(self.size/2),int(self.size/2)])
    # The agent's target location is three Manhattan Distances away from the initial location
    while True:
        self.target_location = self.np_random.integers(0, self.size, size=2, dtype=int)
        if abs(self.target_location[0] - self.agent_location[0]) + abs(self.target_location[1] - self.agent_location[1]) == 3:
            break

    # reset board
    self.board = np.random.randint(low=0, high=4, size=(self.size, self.size))

    # reset chips list
    for i in range(self.agent_num):
        # 0:white 1:red 2:green 3:blue
        self.chip_list[i] = allocation_amount(4, 4)

    while np.array_equal(self.target_location, self.agent_location):
        self.target_location = self.np_random.integers(
            0, self.size, size=2, dtype=int
        )

    observation = self.get_obs()
    info = self.get_info()

    if self.render_mode == "human":
        self.render_frame()

    return observation, info

