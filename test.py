'''
Testing file of colored trail game
'''
import unittest
import numpy as np
import gymnasium as gym
from  colored_trail import agents
from colored_trail.policy import random_policy
import random
import numpy as np



class TestColorTrail(unittest.TestCase):
    def setUp(self):
        '''
        Only test 2 agent situation
        '''
        self.env = gym.make("colored_trail/ColoredTrailEnv-v0", render_mode=None, size=5, agent_num = 2)
        self.ori_observation, self.ori_info = self.env.reset(seed=42)
        #print(self.ori_observation)

    def test_stay(self):
        '''
        testing stay action
        '''
        # stay action
        action_list = [4, 4]
        observation, reward_list, terminated, truncated, info = self.env.step(action_list)
        ori_agent_0 = self.ori_observation[0]
        ori_agent_1 = self.ori_observation[1]
        agent_0 = observation[0]
        agent_1 = observation[1]

        assert agent_0['my_idx'] == ori_agent_0['my_idx']
        assert agent_1['my_idx'] == ori_agent_1['my_idx']

        np.testing.assert_array_equal(agent_0['my_loc'], ori_agent_0['my_loc'],)
        np.testing.assert_array_equal(agent_1['my_loc'], ori_agent_1['my_loc'],)

        np.testing.assert_array_equal(agent_0['my_target'], ori_agent_0['my_target'],)
        np.testing.assert_array_equal(agent_1['my_target'], ori_agent_1['my_target'],)

        np.testing.assert_array_equal(agent_0['my_chips'], ori_agent_0['my_chips'],)
        np.testing.assert_array_equal(agent_1['my_chips'], ori_agent_1['my_chips'],)

        np.testing.assert_array_equal(agent_0['other_loc'][1], ori_agent_0['other_loc'][1],)
        np.testing.assert_array_equal(agent_1['other_loc'][0], ori_agent_1['other_loc'][0],)

        np.testing.assert_array_equal(agent_1['other_loc'][0], agent_0['my_loc'],)
        np.testing.assert_array_equal(agent_0['other_loc'][1], agent_1['my_loc'],)
    def test_move(self):
        '''
        test moving action
        '''
        # agent 0 move right
        # agent 1 move up
        self.env.unwrapped.agent_location_list = {0:np.array([1,1]), 
                                                    1:np.array([2,3])}

        self.env.unwrapped.chip_list = {0:np.array([2,2,2,2]), 1: np.array([2,2,2,2])}

        action_list = [0, 1]
        observation, reward_list, terminated, truncated, info = self.env.step(action_list)
        agent_0 = observation[0]
        agent_1 = observation[1]

        np.testing.assert_array_equal(agent_0['my_loc'], np.array([2,1]))
        np.testing.assert_array_equal(agent_1['my_loc'], np.array([2,4]))

        np.testing.assert_array_equal(agent_1['other_loc'][0], np.array([2,1]))
        np.testing.assert_array_equal(agent_0['other_loc'][1], np.array([2,4]))

        action_list = [1,1]
        observation, reward_list, terminated, truncated, info = self.env.step(action_list)

        agent_0 = observation[0]
        agent_1 = observation[1]

        np.testing.assert_array_equal(agent_0['my_loc'], np.array([2,2]))
        np.testing.assert_array_equal(agent_1['my_loc'], np.array([2,4]))

    def test_contract(self):
        '''
        Test contract
        '''

        #self.env.unwrapped.agent_location_list = {0:np.array([1,1]), 
        #                                            1:np.array([2,3])}
        self.env.unwrapped.chip_list = {0:np.array([1,1,1,1]), 1: np.array([1,1,1,1])}
        # (0,1,1,1)
        # stay
        action_list = [5, 4]
        observation, reward_list, terminated, truncated, info = self.env.step(action_list)
        agent_1 = observation[1]

        action_list = [4, 305]

        observation, reward_list, terminated, truncated, info = self.env.step(action_list)

        agent_0 = observation[0]
        agent_1 = observation[1]

        np.testing.assert_array_equal(agent_0['my_chips'], np.array([0,2,1,1]))
        np.testing.assert_array_equal(agent_1['my_chips'], np.array([2,0,1,1]))








if __name__ == '__main__':
    unittest.main()
        




