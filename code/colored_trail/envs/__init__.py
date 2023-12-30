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

    def __init__(self, render_mode=None, size=5, agent_num=1):
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

        # size of the PyGame window
        self.window_size = 512  

        # each agent has a chip list, which is a list of dictionaries
        # a specific chip is needed for a passing a specific color of block
        self.chip_list = self.ini_chip_list()


        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2.
        # Each block of the whole board has 4 colors: white, red, green, blue 
        # 0: white, 1: red, 2: green, 3: blue
        self.board = np.random.randint(low=0, high=4, size=(size, size))
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                # the whole board
                "board": spaces.Discrete(self.size*self.size*4)
           }
        )

        # We have 5 actions, corresponding to "right", "up", "left", "down", "negotiation"
        # TODO: change to 5 actions, add negotiation action
        self.action_space = spaces.Discrete(4)

    
        self.action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
    from ._render import render_frame
    from ._reset import reset
    from ._step import step
    from ._close import close
    from ._get import get_obs, get_info
    def ini_chip_list(self):
        '''
        Initialize the chip list
        Return:
            chip_list: list of dictionaries
        '''
        # TODO: change to a new initialize method
        # NOTE: leave to the end
        chip_list = [{'red': 0, 'green': 0, 'blue': 0} for i in range(self.agent_num)]

        return chip_list




