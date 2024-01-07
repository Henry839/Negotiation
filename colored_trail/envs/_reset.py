'''
reset method of the environment
Reset the environment after 'done'
'''
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np
def sample_target_location(self, agent_location):
    '''
    sample a target location for the agent
    the target location is three Manhattan Distances away from the initial location
    Parameters:
        agent_location: the starting location of the agent
    Return:
        target_location: the target location of the agent
    '''
    while True:
        target_location = self.np_random.integers(0, self.size, size=2, dtype=int)
        if abs(target_location[0] - agent_location[0]) +  \
        abs(target_location[1] - agent_location[1]) == 3:
            break
    # print("target_location:",target_location)
    return target_location



def reset(self, idx = 0, seed=None, options=None):
    super(type(self), self).reset(seed=seed)

    # The agent always starts at the center of the board
    self.agent_location_list = [np.array([int(self.size / 2), int(self.size / 2)])
                                for i in range(self.agent_num)]
    # sample agent and target locations
    self.target_location_list = [self.sample_target_location(agent_location)
                                 for agent_location in self.agent_location_list]

    # reset board
    self.board = np.random.randint(low=0, high=4, size=(self.size, self.size))

    # reset chips list
    for i in range(self.agent_num):
        # 0:white 1:red 2:green 3:blue
        self.chip_list[i] = self.ini_chip(4, 4)

    observation = self.get_obs(idx)

    info = self.get_info()

    if self.render_mode == "human":
        self.render_frame()

    return observation, info

