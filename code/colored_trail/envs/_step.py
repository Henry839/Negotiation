'''
step function:
after receiving an action and update the env
Parameters: 
    action: the action taken by the agent
Return:
    observation: the observation of the env
    reward: the reward of the env
    terminated: whether the env is terminated
    info: the info of the env
'''
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np

def step(self, action):
    # TODO: Judge whether the action is valid
    # TODO: the judgement should consider the agent's chip list (see __init__.py)

    # map action to direction (see __init__.py)
    direction = self.action_to_direction[action]
    self.agent_location = np.clip(self.agent_location + direction, 0, self.size - 1)

    # An episode is done if the agent has reached the target
    terminated = np.array_equal(self.agent_location, self.target_location)
    reward = 1 if terminated else 0  # Binary sparse rewards
    observation = self.get_obs()
    info = self.get_info()

    if self.render_mode == "human":
        self.render_frame()

    return observation, reward, terminated, False, info


