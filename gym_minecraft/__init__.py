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


Eight rooms of approximately the same size are connected by openings or doors
(with switches to open or not). All rooms are at the same level. There might
also be lava and water around that has to be surrounded. There is a target
block placed somewhere in the last room. Spawning zombies, witches, etc.,
disabled.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to get
killed, Positive if the target block is touched (+4000) and negative if the
time is over (-1000). There's a small reward (+20) for touching the target
block.

Ends:
Task ends if target block is reached. Or if the timeLimitMs=45000 (45 sec.) is
reached.

Observability:
Partial observability. Currently using VideoProducer (320x240).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving on the flat surface required and the
"use" action needed to open the doors. Jumping is not necessary but useful.
"""
)

add_task(
    id='MinecraftAttic-v0',
    group='minecraft',
    summary='Attic!',
    description="""
Two rooms (one above the other) of different sizes connected by a stair of
blocks (where steps are not consecutive and one can fall). Rooms are at
different levels. There are some small walls with lava around that have to be
jumped. There is a target block placed somewhere in the upstairs room. Spawning
zombies, witches, etc., disabled.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block"). Because of the seed, it is always "gold_block".

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to get
killed, Positive if the target block is touched (+1000) and negative if the
time is over (-1000). There's a small reward (+20) for touching the target
block.

Ends:
Task ends if target block is reached. Or if the timeLimitMs=30000 (30 sec.) is
reached.

Observability:
Partial observability. Currently using VideoProducer (320x240).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving and jumping are necessary.
"""
)

add_task(
    id='MinecraftVertical-v0',
    group='minecraft',
    summary='Vertical!',
    description="""
Three rooms (each above the other) of similar size connected by stairs (with a
corner) and a straight vertical ladder. The three rooms are at different
levels. There is a target block placed somewhere in the topmost room. Spawning
zombies, witches, etc., disabled.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to get
killed, Positive if the target block is touched (+8000) and negative if the
time is over (-1000). There's a small reward (+20) for touching the target
block.

Ends:
Task ends if target block is reached. Or if the timeLimitMs=45000 (45 sec.) is
reached.

Observability:
Partial observability. Currently using VideoProducer (320x240).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving (including pitching up for climbing
ladders) and jumping are necessary.
"""
)

add_task(
    id='MinecraftComplexityUsage-v0',
    group='minecraft',
    summary='Complexity usage!',
    description="""
Several rooms of different sizes connected by doors (with switches to open or
not) and stairs or ladders. Rooms are at different levels. There might also be
lava around and some small walls that have to be jumped. There is a target
block placed somewhere in one room. Spawning zombies, witches, etc., disabled.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to get
killed, Positive if the target block is touched (+1000) and negative if the
time is over (-1000). There's a small reward (+20) for touching the target
block.

Ends:
Task ends if target block is reached. Or if the timeLimitMs=30000 (30 sec.) is
reached.

Observability:
Partial observability. Currently using VideoProducer (320x240).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving (including pitching up for climbing
ladders) and jumping are necessary.
"""
)

add_task(
    id='MinecraftMedium-v0',
    group='minecraft',
    summary='Medium!',
    description="""
14 rooms of different sizes connected by doors (with switches to open or not)
and stairs or ladders. There might also be lava and water around and some small
walls that have to be jumped, also some rooms are also accessible by jumping
from blocks to blocks. There is a target block placed somewhere in one room.
Spawning zombies, witches, etc., disabled.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to get
killed, Positive if the target block is touched (+16000) and negative if the
time is over (-1000). There's a small reward (+20) for touching the target
block.

Ends:
Task ends if target block is reached. Or if the timeLimitMs=90000 (90 sec.) is
reached.

Observability:
Partial observability. Currently using VideoProducer (320x240).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving (including pitching up for climbing
ladders) and jumping are necessary.
"""
)

add_task(
    id='MinecraftHard-v0',
    group='minecraft',
    summary='Hard!',
    description="""
32 rooms of different sizes connected by doors (with switches to open or not)
and stairs or ladders. There might also be lava and water around and some small
walls that have to be jumped, also some rooms are also accessible by jumping
from blocks to blocks. There is a target block placed somewhere in one room.
Spawning zombies, witches, etc., disabled.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to get
killed, Positive if the target block is touched (+32000) and negative if the
time is over (-1000). There's a small reward (+20) for touching the target
block.

Ends:
Task ends if target block is reached. Or if the timeLimitMs=120000 (120 sec.) is
reached.

Observability:
Partial observability. Currently using VideoProducer (320x240).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving (including pitching up for climbing
ladders) and jumping are necessary.
"""
)
