"""
step function:
after receiving an action and update the env
Parameters:
    action: the action taken by the agent
Return:
    observation: the observation of the env
    reward: the reward of the env
    terminated: whether the env is terminated
    info: the info of the env
"""
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np


def color(action):  # Match the relevant actions in the negotiation with the color of the chips
    if action < 8:
        return 0
    if action < 12:
        return 1
    if action < 16:
        return 2
    if action < 20:
        return 3


def step(self, action):
    if action < 4:  # move action
        next_position = self.agent_location + self.action_to_direction[action]
        # Judge whether the move action is valid
        if next_position[0] < 0 or next_position[0] >= self.size or next_position[1] < 0 \
                or next_position[1] >= self.size:
            reward = -1
            terminated = 0
        # the judgement consider the agent's chip list (see __init__.py)
        elif self.chip_list[0][self.board[next_position[0]][next_position[1]]] <= 0:
            reward = -1
            terminated = 0
        else:
            self.chip_list[0][self.board[next_position[0]][next_position[1]]] -= 1
            # map action to direction (see __init__.py)
            direction = self.action_to_direction[action]
            self.agent_location = np.clip(self.agent_location + direction, 0, self.size - 1)
            # An episode is done if the agent has reached the target
            terminated = np.array_equal(self.agent_location, self.target_location)
            reward = 1 if terminated else 0  # Binary sparse rewards
    else:  # the relevant actions in the negotiation
        if self.chip_list[0].sum() == 0:  # An episode is done if the total number of chips is 0.
            reward = -10
            terminated = 1
        else:
            # Find the block for the negotiation action
            direction = self.action_to_direction[(action - 4) % 4]
            next_position = self.agent_location + direction
            # Judge whether the negotiation action is valid
            if self.chip_list[0][color(action)] <= 0 or next_position[0] < 0 or next_position[0] >= self.size \
                    or next_position[1] < 0 or next_position[1] >= self.size:
                reward = -1
                terminated = 0
            else:
                # swap one chip for another chip. Note that the assumption here is that the environment automatically
                # agrees to the exchange as long as the action is valid
                self.chip_list[0][color(action)] -= 1
                self.chip_list[0][self.board[next_position[0]][next_position[1]]] += 1
                reward = -0.1
                terminated = 0
    observation = self.get_obs()
    info = self.get_info()

    if self.render_mode == "human":
        self.render_frame()

    return observation, reward, terminated, False, info
