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



def reset(self, seed=None):
    '''
    Reset function of the environment
    Parameters:
        seed: int, the seed of the environment
    Return:
        observation: list, the observation of each agent on the environment
        info: array, the distance info of the environment
    '''
    super(type(self), self).reset(seed=seed)

    # sample agent init location
    self.agent_location_list = {i: (self.np_random.integers(0, self.size, size=2, dtype=int))
                                for i in range(self.agent_num)}
    # sample agent and target locations
    self.target_location_list = {i: self.sample_target_location(self.agent_location_list[i])
                                 for i in range(self.agent_num)}

    # reset board
    self.board = np.random.randint(low=0, high=4, size=(self.size, self.size))

    # reset chips list
    self.chip_list = {i : self.ini_chip(type = 4, amount = 4) 
                          for i in range(self.agent_num)}
    # each proposal is empty proposal
    self.proposals_list = {i:{'color_out':0,
                              'color_in':0,
                              'out_num':0,
                              'in_num':0,
                              }
                           for i in range(self.agent_num)}
    # unvalid responses
    self.responses_list = {i: i
                           for i in range(self.agent_num)}


    # observation list of each agent
    observation = self.get_obs()

    # distance info
    info = self.get_info()

    if self.render_mode == "human":
        self.render_frame()
    return observation, info

