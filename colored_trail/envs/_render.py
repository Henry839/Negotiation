"""
The render function for the environemnt.
Implemented by using pygame.
"""
import gymnasium as gym
from gymnasium import spaces

import pygame
import numpy as np


def render_frame(self):
    if self.window is None and self.render_mode == "human":
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
    if self.clock is None and self.render_mode == "human":
        self.clock = pygame.time.Clock()
    pix_square_size = (
            self.window_size / self.size
    )  # The size of a single grid square in pixels
    canvas = pygame.Surface((self.window_size, self.window_size))
    canvas.fill((255, 255, 255))

    # Implement colored blocks
    for i in range(self.size):
        for j in range(self.size):
            if self.board[i][j] == 1:
                pygame.draw.rect(
                    canvas,
                    (255, 0, 0),
                    pygame.Rect(
                        pix_square_size * np.array([i, j]),
                        (pix_square_size, pix_square_size),
                    ),
                )
            if self.board[i][j] == 2:
                pygame.draw.rect(
                    canvas,
                    (0, 255, 0),
                    pygame.Rect(
                        pix_square_size * np.array([i, j]),
                        (pix_square_size, pix_square_size),
                    ),
                )
            if self.board[i][j] == 3:
                pygame.draw.rect(
                    canvas,
                    (0, 0, 255),
                    pygame.Rect(
                        pix_square_size * np.array([i, j]),
                        (pix_square_size, pix_square_size),
                    ),
                )

    for i in range(self.agent_num):
        # First we draw the target
        pygame.draw.circle(
            canvas,
            (192, 192, 192),
            (self.target_location_list[i] + 0.5) * pix_square_size,
            pix_square_size / 3,
        )
        # Now we draw the agent
        pygame.draw.circle(
            canvas,
            (0, 0, 0),
            (self.agent_location_list[i] + 0.5) * pix_square_size,
            pix_square_size / 3,
        )

    # Finally, add some gridlines
    for x in range(self.size + 1):
        pygame.draw.line(
            canvas,
            0,
            (0, pix_square_size * x),
            (self.window_size, pix_square_size * x),
            width=3,
        )
        pygame.draw.line(
            canvas,
            0,
            (pix_square_size * x, 0),
            (pix_square_size * x, self.window_size),
            width=3,
        )

    if self.render_mode == "human":
        # The following line copies our drawings from `canvas` to the visible window
        self.window.blit(canvas, canvas.get_rect())
        pygame.event.pump()
        pygame.display.update()

        # We need to ensure that human-rendering occurs at the predefined framerate.
        # The following line will automatically add a delay to keep the framerate stable.
        self.clock.tick(self.metadata["render_fps"])
    else:  # rgb_array
        return np.transpose(
            np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
        )
