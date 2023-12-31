from gymnasium.envs.registration import register

register(
    id="colored_trail/ColoredTrailEnv-v0",
    entry_point="colored_trail.envs:ColoredTrailEnv",
    max_episode_steps=300,
)
