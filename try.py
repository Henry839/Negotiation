import gymnasium as gym
import colored_trail

env = gym.make("colored_trail/ColoredTrailEnv-v0", render_mode="human", size=5)
observation, info = env.reset(seed=42)
for _ in range(1000):
    action = env.action_space.sample()  # this is where you would insert your policy
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()
env.close()
