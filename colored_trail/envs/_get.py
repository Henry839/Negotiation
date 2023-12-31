import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np

def get_obs(self):
    return {"agent": self.agent_location, "target": self.target_location, "board": self.board}

def get_info(self):
        return {
            "distance": np.linalg.norm(
                self.agent_location - self.target_location, ord=1
            )
        }

