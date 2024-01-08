"""
Done
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
        agent_location: location before the move action
        target_location: the target place of the agent
        idx: index of the agent
    Return:
        next_position
        terminated: boolean
        reward
    '''
    if action == 4:
        # stay
        return agent_location, 0, 0
    next_position = np.clip(agent_location + self.action_to_direction[action], 0, self.size - 1)
    reward = 0
    if self.chip_list[idx][self.board[next_position[0]][next_position[1]]] <= 0:
        # hasn't got the corresponding chip
        terminated = 0
        next_position = agent_location
    else:
        # success
        self.chip_list[idx][self.board[next_position[0]][next_position[1]]] -= 1

        # An episode is done if the agent has reached the target
        terminated = np.array_equal(agent_location, target_location)
        if terminated:
            reward = 1

    return next_position, terminated, reward


def contract_execute(self, proposer, responder, contract):
    '''
    Execute the contract, exchange the chips between proposer and responder
    Parameters:
        proposer: int 
        responder: int
        contract: (color_out, color_in, out_num, in_num)
    Return:
        True: excution success
        False: excution failed
    Note: "out" corresponds to what should the proposer pays, and "in" corresponds to what can the proposer get
    '''
    # judge the validity of the contract
    if self.chip_list[proposer][contract['color_out']] < contract['out_num'] or \
        self.chip_list[responder][contract['color_in']] < contract['in_num']:
        return False

    # proposer
    self.chip_list[proposer][contract['color_out']] -= contract['out_num']
    self.chip_list[proposer][contract['color_in']] += contract['in_num']

    # responder
    self.chip_list[responder][contract['color_out']] += contract['out_num']
    self.chip_list[responder][contract['color_in']] -= contract['in_num']
    return True


def step(self, action_n):
    '''
    After receiving the action_n and update env
    Parameters:
        action_n: list, the actions taken by the agents
    Return:
        observation: the observation of the env
        reward: the reward of the env
        terminated: whether the env is terminated
        info: the info of the env

    '''
    reward_list = [0 for _ in range(self.agent_num)]
    new_proposals_list = {i: {'color_out': 0, 'color_in': 0, 'out_num': 0, 'in_num': 0}
                          for i in range(self.agent_num)}
    new_responses_list = {i:i for i in range(self.agent_num)}
    terminated = 0

    for i, action in enumerate(action_n):
        # empty propose
        proposal = {'color_out': 0, 'color_in': 0, 'out_num': 0, 'in_num': 0}
        proposer = i

        if action < 5: # move action
            self.agent_location_list[i], terminated, reward = self.move(action, 
                                                                        self.agent_location_list[i],
                                                                        self.target_location_list[i],
                                                                        i)
            reward_list[i] += reward

        elif action >= 5 and action < 305: # propose action 
            proposal = self.action_to_propose[action]
            proposal = {'color_out': proposal[0], 'color_in': proposal[1], 'out_num': proposal[2], 'in_num': proposal[3]}

        elif action >= 305: # response action
            # as an agreement is formed, a contract appears! Hurah!
            proposer = self.action_to_response[action]

            if proposer != i:
                # proposer == i represents refuse all
                contract = self.proposals_list[proposer]
                # execute the contract
                exc =  self.contract_execute(proposer, i, contract)
                if exc:
                    # successful contract, reward++ for both side
                    reward_list[proposer] += 1
                    reward_list[i] += 1
                else:
                    # failed contract, reward-- for both side
                    reward_list[proposer] -= 1
                    reward_list[i] -= 1

        # update response list
        new_responses_list[i] = proposer
        # update proposal list
        new_proposals_list[i] = proposal

    self.proposals_list = new_proposals_list
    self.responses_list = new_responses_list



    if not terminated: 
        # if nobody reach their targets, check whether somebody's chip num is 0
        check = 1 if 0 in [sum(self.chip_list[i]) for i in range(self.agent_num)] else 0
        terminated = check
        if terminated == 1:
            # if somebody's chip num is 0, the game is over
            for j in range(self.agent_num):
                reward_list[j] -= 1

        
        
    if self.render_mode == "human":
        self.render_frame()

    info = self.get_info()
    observation = self.get_obs()
    return observation, reward_list, terminated, False, info
