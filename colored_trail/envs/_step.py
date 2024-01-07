"""
Not Done
"""
# TODO:  write the part of negotiation in step function
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np

def move(self, action, agent_location,target_location,idx):
    '''
    Moving action of the agent
    Parameters:
        action: the action taken by the agent
    Return:
        next_position
        terminated: boolean
    '''
    next_position = np.clip(agent_location + self.action_to_direction[action], 0, self.size - 1)
    reward = 0
    if self.chip_list[idx][self.board[next_position[0]][next_position[1]]] <= 0:
        terminated = 0
        next_position = agent_location
    else:
        self.chip_list[idx][self.board[next_position[0]][next_position[1]]] -= 1
        # An episode is done if the agent has reached the target
        terminated = np.array_equal(agent_location, target_location)
        if terminated:
            reward = 1

    return next_position, terminated, reward

# TODO: The end of the game should take into account the fact that neither side's chips will help them move
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
    Flag = False
    reward = 0
    for i, action in enumerate(action_n):
        if action == None:
            terminated = 0
        elif action[4:8] == [0,0,0,0]:
            if action[0] < 4: # move action
                self.agent_location_list[i], terminated, reward = self.move(action[0], self.agent_location_list[i],
                                                                            self.target_location_list[i],i)
                print(self.chip_list)
            elif action[0] == 4: # agree
                # exchange chips
                chips = self.observation["proposal"]
                for j in range(4):
                    self.chip_list[i][j] += chips[j]
                    self.chip_list[i][j] -= chips[4 + j]
                    self.chip_list[1 - i][j] -= chips[j]
                    self.chip_list[1 - i][j] += chips[4 + j]
                terminated = 0
            elif action[0] == 5: # disagree
                terminated = 0
        else:  # the exchange actions
            if self.chip_list[i].tolist() == [0,0,0,0]:  # An episode is done if the total number of chips is 0.
                terminated = 1
            else:
                # the entrance to add the proposal to the observation
                Flag = True
                reward = -0.1
                terminated = 0
    for i in range(len(action_n)):
        if action_n[i] != None:
            observation = self.get_obs(i)
    if Flag: # add proposal to observation
        for i in range(len(action_n)):
            if action_n[i] != None:
                observation["proposal"] = action_n[i]
    info = self.get_info()

    if terminated: # TODO: At the end of the game, the reward should be calculated according to the rules
        reward = 0

    if self.render_mode == "human":
        self.render_frame()

    return observation, reward, terminated, False, info
