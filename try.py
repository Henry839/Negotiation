import gymnasium as gym
from  colored_trail import agents
from colored_trail.policy import random_policy
import random

env = gym.make("colored_trail/ColoredTrailEnv-v0", render_mode="human", size=5)
observation, info = env.reset(seed=42)
env.observation = observation
agent_num = 2
terminated = True

i = 0
j = 0
Flag = True
tmp = 1
while i < 1000 and j < 1000:
    action_list = []
    # alternating offers
    if i == 0: # Eliminate the first-mover advantage
        if tmp:
            action1 = random_policy.Alice(observation)
            action2 = None
        else:
            action2 = random_policy.Alice(observation)
            action1 = None
            flag = False
    else:
        if Flag:
            if i%2 == 0: # agent1 choose action
                action1 = random_policy.Alice(observation)
                action2 = None
            else: # agent2 choose action
                action2 = random_policy.Alice(observation)
                action1 = None
        else:
            if i%2 == 1: # agent1 choose action
                action1 = random_policy.Alice(observation)
                action2 = None
            else: # agent2 choose action
                action2 = random_policy.Alice(observation)
                action1 = None
    action_list.append(action1)
    action_list.append(action2)
    observation, reward, terminated, truncated, info = env.step(action_list)
    env.observation = observation

    if terminated or truncated:
        tmp = random.randint(0, 1)
        observation, info = env.reset(idx=tmp)
        env.observation = observation
        i = 0

    i += 1
    j += 1

env.close()
