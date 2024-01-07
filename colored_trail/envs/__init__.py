'''
init method of ColoredTrailEnv
code coming from tutorial of gymnasium
'''
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np

class ColoredTrailEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=5, agent_num=2):
        ''' Parameters:
            render_mode: str
            size: int, board size
            agent_num: int, number of agents
        '''
        # size of the square grid
        self.size = size

        # number of the agents in the environment
        self.agent_num = agent_num
        self.agent_location_list = []
        self.agent_direction_list = []

        # size of the PyGame window
        # self.window_size = 512
        self.window_size = 256

        # each agent has a chip list, which is a list of dictionaries
        # a specific chip is needed for a passing a specific color of block
        self.chip_list = [self.ini_chip(4, 4) for i in range(agent_num)]

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2.
        # Each block of the whole board has 4 colors: white, red, green, blue 
        # 0: white, 1: red, 2: green, 3: blue
        self.board = np.random.randint(low=0, high=4, size=(size, size))
        self.observation_space = spaces.Dict(
            {
                "my_agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "my_target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                # the whole board
                "board": spaces.Discrete(self.size * self.size * 4),
                "other_agent":spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "my_chips": spaces.Box(0, 3, shape=(4,), dtype=int),
                "other_chips": spaces.Box(0, 3, shape=(4,), dtype=int),
                "proposal": spaces.Box(0, 3, shape=(8,), dtype=int)
            }
        )

        """ We have 4 moving actions, corresponding to "right", "up", "left", "down", "negotiation"
            change to  actions, add negotiation+direction+chip action
            eg: 4:negotiation+right+white 5:negotiation+up+white 8:negotiation+right+white 9:negotiation+up+white
            'negotiation+right+white' means 'swap one white chip for the chip on the right side of the agent_position'
            NOTE: Do it after the implementation color blocks part is done
        """
        # TODO: Change action space to color to color, see _step()
        """
        允许看见交易对方的筹码，动作空间根据当前的状态来定的
        """
        self.action_space = spaces.Discrete(20)

        self.action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }
        self.observation = {"proposal":[0,0,0,0,0,0,0,0]}
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    from ._render import render_frame
    from ._reset import reset, sample_target_location
    from ._step import step, move
    from ._close import close
    from ._get import get_obs, get_info
    def ini_chip(self, num_people, amount):
        '''
        Initialize the chip list
        Return:
            chip: allocated chip num
        '''
        a = [np.random.randint(0, amount) for i in range(num_people-1)] + [0, amount]
        a.sort()
        chip = np.array([a[i+1]-a[i] for i in range(num_people)])
        return chip 
