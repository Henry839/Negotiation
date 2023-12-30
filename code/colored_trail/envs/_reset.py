'''
reset method of the environment
Reset the environment after 'done'
'''
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np


def reset(self, seed=None, options=None):
    super(type(self), self).reset(seed=seed)

    # sample agent and target locations
    self.agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)
    self.target_location = self.agent_location

    # reset board
    self.board = np.random.randint(low=0, high=4, size=(self.size, self.size))

    # reset chips list
    self.chip_list = [{'red': 0, 'green': 0, 'blue': 0} for i in range(self.agent_num)]


    while np.array_equal(self.target_location, self.agent_location):
        self.target_location = self.np_random.integers(
            0, self.size, size=2, dtype=int
        )

    observation = self.get_obs()
    info = self.get_info()

    if self.render_mode == "human":
        self.render_frame()

    return observation, info

