'''
init method of ColoredTrailEnv
code coming from tutorial of gymnasium
'''
import gymnasium as gym
from gymnasium.spaces import Dict, Box, Discrete
import pygame
import numpy as np

class ColoredTrailEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, 
                 render_mode=None, 
                 size=5, 
                 agent_num=2,):
        ''' 
        Parameters:
            render_mode: str
            size: int, board size
            agent_num: int, number of agents
        '''
        # size of the square grid
        self.size = size

        # number of the agents in the environment
        self.agent_num = agent_num
        self.agent_list = [i for i in range(self.agent_num)]

        # size of the PyGame window
        self.window_size = 256


        # 0: white, 1: red, 2: green, 3: blue
        self.board = np.random.randint(low=0, high=4, size=(size, size))
        self.chip_list = {i : self.ini_chip(type = 4, amount = 4) 
                          for i in range(agent_num)}
        self.agent_location_list = {i: (0,0) for i in range(agent_num)}
        self.target_location_list = {i: (0,0) for i in range(agent_num)}
        # empty proposal
        self.proposals_list = {i: {'color_out': 0, 
                                  'color_in': 0, 
                                  'out_num': 0, 
                                  'in_num': 0}
                              for i in range(agent_num)}
        # idx_of_agent: the agent it agrees
        # choosing the same number as its idx means refuse everybody
        self.responses_list = {i: i
                               for i in range(agent_num)}

        # spaces: (1) Observation space (2) Action space
        self.observation_space = Dict(
                {
                    key: Dict({
                        "my_idx": Discrete(self.agent_num),
                        "my_loc": Box(0, size - 1, shape=(2,), dtype=int),
                        "my_target": Box(0, size - 1, shape=(2,), dtype=int),
                        "my_chips": Box(0, 10000, shape=(4,), dtype=int),
                        "board": Discrete(self.size * self.size * 4),
                        "other_loc": Dict({
                            key2: Box(0, size - 1, shape=(2,), dtype=int)
                            for key2 in self.agent_list
                            if key2 != key
                            }),
                        "other_chips": Dict({
                            key3: Box(0, 10000, shape=(4,), dtype=int)
                            for key3 in self.agent_list
                            if key3 != key
                            }),
                        "proposals": Dict({
                            key1:Dict({
                                "color_out": Discrete(4),
                                "color_in": Discrete(4),
                                "out_num": Discrete(5),
                                "in_num": Discrete(5),
                                })
                                for key1 in self.agent_list
                                if key1 != key
                                }),
                        # response is which agent the others agree
                        # choosing my_idx: refuse all
                        "responses": Dict({
                            key4: Discrete(self.agent_num)
                            for key4 in self.agent_list
                            if key4 != key
                            }),
                            })
                    for key in self.agent_list
                    }
        )

        """ 
        拉平版本: 若要改成层次版本，多写几个action space即可
        Moving action: 5 (up, down, right, left, stay)
        Proposer action: 4 * 3 * 5 * 5 = 300
            Eg: (0,1,1,5): 1 white to 5 red, 
            Eg: (1,2,3,4): 3 red to 4 green
        Responder action: self.agent_num
        Note: 
            (1) The maximum amount of chip change is 5 
            (2) For a responder, the proposal is a 4 * 2 matrix

        """
        self.action_space = Dict(
                {
                    key: Discrete(305 + self.agent_num + 1)
                    for key in self.agent_list
                    }
        )

        # mapping function: map num to real action
        self.action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
            4: np.array([0, 0]),
        }
        # 300 actions
        propose = [(color_out, color_in, out_num, in_num) 
                    for color_out in range(0,4)
                    for color_in in range(0,4)
                    for out_num in range(1, 6)
                    for in_num in range(1, 6)
                    if color_out != color_in
             ]
        self.action_to_propose =  {key+5: value for key, value in enumerate(propose)}
        self.action_to_response = {key + 305: key for key in range(self.agent_num)}

        # rendering
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None
    from ._render import render_frame
    from ._reset import reset, sample_target_location
    from ._step import step, move, contract_execute
    from ._close import close
    from ._get import get_obs, get_info, _get_observation

    def ini_chip(self, type, amount):
        '''
        Initialize the chip of a single agent
        Parameters:
            type: int, number of chip types
            amount: int, number of chips
        Return:
            chip: allocated chip  list 
                    eg: type = 4, amount = 3
                    chip = [0, 1, 0, 2]
                    means 1 red, 2 green
        '''
        a = [np.random.randint(0, amount) for i in range(type-1)] + [0, amount]
        a.sort()
        chip = np.array([a[i+1]-a[i] for i in range(type)])
        return chip 
