'''
The close method of the environment.
'''
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np

def close(self):
    if self.window is not None:
        pygame.display.quit()
        pygame.quit()
