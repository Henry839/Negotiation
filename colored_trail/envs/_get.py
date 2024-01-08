import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np

def get_obs(self):
    '''
    Get the observation of the current state of the whole environment.
    Return:
        dict, {key: observation}
        key: int, the idx of agents
    '''
    obs = {key: self._get_observation(key) 
            for key in range(self.agent_num)}



    return obs
def _get_observation(self, idx):
    '''
    Private func for get_obs. return the observation of the idx agent 
    Parameters:
        idx: int, the idx of agents
    Return:
        obs: dict, the observation of the idx agent
    '''
    obs ={
            "my_idx": idx, 
            "my_loc": self.agent_location_list[idx],
            "my_target": self.target_location_list[idx],
            "my_chips": self.chip_list[idx],
            "board": self.board,
            "other_loc": {i: self.agent_location_list[i]
                          for i in range(self.agent_num) if i != idx},
            "other_chips": {i: self.chip_list[i]
                            for i in range(self.agent_num) if i != idx},
            "proposals": {i: self.proposals_list[i] 
                          for i in range(self.agent_num) if i != idx},
            "responses": {i: self.responses_list[i]
                          for i in range(self.agent_num) if i != idx},
            }
    return obs

def get_info(self):
    '''
    Distance info
    '''
    return {
        "distance": np.linalg.norm(
            [self.agent_location_list[i] - self.target_location_list[i] for i in range(self.agent_num)], ord=1
        )
    }

