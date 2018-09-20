from gym.envs.registration import register


# Env registration
# ==========================

register(
    id='MinecraftDefaultWorld1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'default_world_1.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 6060},
    #timestep_limit=6060,
    reward_threshold=1000
)

register(
    id='MinecraftDefaultFlat1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'default_flat_1.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 2020},
    #timestep_limit=2020,
    reward_threshold=100
)

register(
    id='MinecraftTrickyArena1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'tricky_arena_1.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 303},
    #timestep_limit=303,
    reward_threshold=300
)

register(
    id='MinecraftEating1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'eating_1.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 303},
    #timestep_limit=303,
    reward_threshold=70
)

register(
    id='MinecraftCliffWalking1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'cliff_walking_1.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 404},
    #timestep_limit=404,
    reward_threshold=100
)

register(
    id='MinecraftMaze1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'maze_1.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 606},
    #timestep_limit=606,
    reward_threshold=1000
)

register(
    id='MinecraftMaze2-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'maze_2.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 2020},
    #timestep_limit=2020,
    reward_threshold=1000
)

register(
    id='MinecraftBasic-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'basic.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 606},
    #timestep_limit=606,
    reward_threshold=980
)

register(
    id='MinecraftObstacles-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'obstacles.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 909},
    #timestep_limit=909,
    reward_threshold=2000
)

register(
    id='MinecraftSimpleRoomMaze-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'simpleRoomMaze.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 909},
    #timestep_limit=909,
    reward_threshold=4000
)

register(
    id='MinecraftAttic-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'attic.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 606},
    #timestep_limit=606,
    reward_threshold=1000
)

register(
    id='MinecraftVertical-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'vertical.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 909},
    #timestep_limit=909,
    reward_threshold=8000
)

register(
    id='MinecraftComplexityUsage-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'complexity_usage.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 606},
    #timestep_limit=606,
    reward_threshold=1000
)

register(
    id='MinecraftMedium-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'medium.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 1818},
    #timestep_limit=1818,
    reward_threshold=16000
)

register(
    id='MinecraftHard-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'hard.xml'},
    #tags={'wrapper_config.TimeLimit.max_episode_steps': 2424},
    #timestep_limit=2424,
    reward_threshold=32000
)


