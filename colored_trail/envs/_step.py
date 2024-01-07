"""
Not Done
"""
# TODO:  write the part of negotiation in step function
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
def move(self, action, agent_location):
    '''
    Moving action of the agent
    Parameters:
        action: the action taken by the agent
    Return:
        next_position
        terminated: boolean
    '''
    next_position = np.clip(agent_location + self.action_to_direction[action], 0, self.size - 1)

    if self.chip_list[0][self.board[next_position[0]][next_position[1]]] <= 0:
        terminated = 0
    else:
        self.chip_list[0][self.board[next_position[0]][next_position[1]]] -= 1
        # An episode is done if the agent has reached the target
        terminated = np.array_equal(agent_location, self.target_location)

    return next_position, terminated


def step(self, action_n):
    '''
    step function:
    after receiving an action and update the env
    Parameters:
        action_n: the actions taken by the agents
    Return:
        observation: the observation of the env
        reward: the reward of the env
        terminated: whether the env is terminated
        info: the info of the env

    '''
    for i, action in enumerate(action_n):
        if action < 4:  # move action
            self.agent_location_list[i], terminated = self.move(action, 
                                                                        self.agent_location_list[i])
        else:  # the relevant actions in the negotiation
            if self.chip_list[0].sum() == 0:  # An episode is done if the total number of chips is 0.
                terminated = 1
            else:
                # Judge whether the negotiation action is valid
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
