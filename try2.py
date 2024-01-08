import gymnasium as gym
from  colored_trail import agents
from colored_trail.policy import random_policy
import random

env = gym.make("colored_trail/ColoredTrailEnv-v0", render_mode="human", size=5, agent_num = 2)
observation, info = env.reset(seed=42)
agent_num = 2
for _ in range(2):
    action_list = env.action_space.sample()
    print(action_list)
    obs = env.observation_space.sample()
    action_list = [action_list[i] for i in range(agent_num)]
    observation, reward_list, terminated, truncated, info = env.step(action_list)

