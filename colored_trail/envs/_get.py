import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np

def get_obs(self,idx):
    return {"my_agent": self.agent_location_list[idx], "my_target": self.target_location_list[idx],
            "board": self.board, "other_agent": self.agent_location_list[1-idx],
            "my_chips": self.chip_list[idx], "other_chips": self.chip_list[1-idx], "proposal": [0,0,0,0,0,0,0,0]}

def get_info(self):
        return {
            "distance": np.linalg.norm(
                [self.agent_location_list[i] - self.target_location_list[i] for i in range(self.agent_num)], ord=1
            )
        }

