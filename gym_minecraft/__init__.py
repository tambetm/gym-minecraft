from gym.envs.registration import register
from gym.scoreboard.registration import add_task, add_group

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

# Scoreboard registration
# ==========================
add_group(
    id='minecraft',
    name='Minecraft',
    description='Minecraft environments based on Malmo.'
)

add_task(
    id='MinecraftDefaultWorld1-v0',
    group='minecraft',
    summary='Survive and find gold, diamond or redstone!',
    description="""
The agent appears in a default Minecraft world, with all possible objects.
The agent appears at x="-204" y="81" z="217", which depending on the world
that is generated means that it's going to fall initially to touch ground.

Goal:
The task instance is considered complete if the agent finds (mines) any
special block (any of "gold_block diamond_block redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), positive if the target block is
touched (+1000) and negative if the time is over (-1000).

End:
Task ends if the timeLimitMs=300000 (300 sec.) is reached or agent killed.

Observability:
Partial observability. Using VideoProducer (480x320).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". Inventory empty initially. So actions are "move", "strafe", "pitch",
"turn", "jump", "crouch", "attack", "use" and "hotbar.X". Action "drop" not
included.
"""
)

add_task(
    id='MinecraftDefaultFlat1-v0',
    group='minecraft',
    summary='Move to a wooden hut in a snow tempest!',
    description="""
The agent appears in a snowy flat landscape and has to survive. The agent
appears at x="0" y="227" z="0".

Goal:
The agent has to reach x="19.5" y="227" z="19.5", which is inside a hut
that is relatively near.

Rewards:
Sparse rewards. Positive +100 given if the goal position is reached.

End:
Task ends if the timeLimitMs=100000 (100 sec.) is reached or agent is killed.

Observability:
Partial observability (although the hut is visible from the beginning).
Using VideoProducer (320x240).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". Inventory empty initially. So actions are "move", "strafe", "pitch",
"turn", "jump", "crouch", "attack", "use" and "hotbar.X". Action "drop" not
included. Only moving on the flat surface required.
"""
)

add_task(
    id='TrickyArena1-v0',
    group='minecraft',
    summary='Mind your step to the redstone!',
    description="""
A flat arena of 40x40 blocks with some of the blocks being special (goals)
or dangerous (lava and water).

Goal:
Touching one of the goal blocks (redstone).

Rewards:
Dense rewards. Positive (+100) if agent steps over obsidian tiles that haven't
been stepped over recently, positive (+400) if goal stone is touched, positive
(+100) if out of the arena, negative (-800) if agent falls into the water,
negative (-900) when time runs out, negative (-1000) if agent dies (e.g.,
falling into the lava).

End:
Task ends if the timeLimitMs=15000 (15 sec.) is reached or agent killed.

Observability:
Partial observability. Using VideoProducer (640x480).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving on the flat surface required.
"""
)

add_task(
    id='Eating1-v0',
    group='minecraft',
    summary='Eat a healthy diet!',
    description="""
A flat world where some food objects are scattered near the starting position.
The good ones must be eaten but not the bad owns.

Goal:
Eating as much as good food items as possible.

Rewards:
Dense rewards. Positive (+2) if agent eats any of "fish porkchop beef chicken
rabbit mutton", positive (+1) if agent eats any of "potato egg carrot",
negative (-1) if agent eats any of "apple melon" and negative (-2) if agent
eats "sugar cake cookie pumpkin_pie".

End:
Task ends if the timeLimitMs=15000 (15 sec.) is reached or agent killed.

Observability:
Partial observability. Using VideoProducer (480x320).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving on the flat surface required.
"""
)

add_task(
    id='CliffWalking1-v0',
    group='minecraft',
    summary='Burning lava!',
    description="""
A cliff of size 12x3 sandstone blocks surrounded by burning lava. Agent must go
from starting block to destination block without following in the lava.

Goal:
The task instance is considered complete if the agent goes from starting
position ("cobblestone") and steps over a special destination block (blue
"lapis_block") without following in the lava.

Rewards:
Sparse rewards. Negative in lava (-100), positive if target block
("lapis_block") touched (+100), and slightly negative (-1) for any action done.
No (negative) reward if out of time.

End:
Task ends if either when fallen in the lava or the destination block is
reached. Or if the timeLimitMs=20000 (20 sec.) is reached.

Observability:
Partial observability for ("ObservationFromGrid", the adjacent cell where the
agent is located) and partial/total for the 3D view ("VideoProducer",
screenshot view). Background is a grey room, surrounding the lava. There are no
torches around but the lava produces some light. Currently using VideoProducer
(640x480).

Actions:
Possible actions given by "ContinuousMovementCommand" included included in
"survival mode". So actions are "move", "strafe", "pitch", "turn", "jump",
"crouch", "use" and "hotbar.X". Action "attack" is forbidden with a
"deny-list". Inventory empty initially. Only moving on the flat surface
required.
"""
)

add_task(
    id='Maze1-v0',
    group='minecraft',
    summary='Get a-mazed!',
    description="""
The agent appears in a maze of size 20x20. Mazes are within walls.

Goal:
The goal must be learnt from rewards. The agent appears at starting position
(emerald_block) and has to traverse the maze to reach the target position
(redstone_block).

Rewards:
Sparse rewards. Negative if dead (-10000), positive if the target block is
touched (+1000) and negative if the time is over (-1000).

End:
Task ends if the timeLimitMs=30000 (30 sec.) is reached or killed.

Observability:
Partial observability. Using VideoProducer (640x480).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving on the flat surface required (jumping
is useless).
"""
)

add_task(
    id='Maze2-v0',
    group='minecraft',
    summary='Get more a-mazed!',
    description="""
The agent appears in a maze of size 64x64. Mazes are different as they can be
labyrinths with walls, or walking on convoluted cliffs surrounded by lava or
water.

Goal:
The agent appears at starting position (emerald_block) and has to traverse the
maze to reach the target position (redstone_block).

Rewards:
Sparse rewards. Negative if dead (-10000), positive if the target block is
touched (+1000) and negative if the time is over (-1000).

End:
Task ends if the timeLimitMs=100000 (100 sec.) is reached or killed.

Observability:
Partial observability. Using VideoProducer (640x480).

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list".
Inventory empty initially. Only moving on the flat surface required (jumping
may be useful in some mazes). Also enabled: <AbsoluteMovementCommands /> and
<DiscreteMovementCommands />.
"""
)

add_task(
    id='MinecraftBasic-v0',
    group='minecraft',
    summary='Grab the treasure!',
    description="""
A room of 7x7x7 surrounded by stone blocks. There is a target block placed
somewhere in the room.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to
get killed, Positive if the target block is touched (+1000) and negative if
the time is over (-1000). There's a small reward (+20) for touching the
target block.

Ends:
Task ends if target block is reached. Or if the timeLimitMs=30000 (30 sec.)
is reached.

Observability:
Partial observability for ("ObservationFromGrid", the adjacent cell where the
agent is located) and partial/total for the 3D view ("VideoProducer",
screenshot view). Background is a grey room, surrounding the lava. There are
no torches around but the lava produces some light. Currently using
VideoProducer (320x240)

Actions:
Possible actions given by "ContinuousMovementCommand" included in "survival
mode". So actions are "move", "strafe", "pitch", "turn", "jump", "crouch",
"use" and "hotbar.X". Action "attack" is forbidden with a "deny-list"
(Issue #70). Inventory empty initially. Only moving on the flat surface
required (jumping is useless).
"""
)

add_task(
    id='MinecraftObstacles-v0',
    group='minecraft',
    summary='The apartment!',
    description="""
Four rooms in a row of approximately the same size connected by openings or
doors (with switches to open or not). All rooms are at the same level. There
might also be lava and water that have to be surrounded. There is a target
block placed somewhere in the last room. Spawning zombies, witches, etc.,
disabled.

Goal:
The task instance is considered complete if the agent goes from starting
position to the special block (any of "gold_block diamond_block
redstone_block").

Rewards:
Sparse rewards. Negative if dead (-10000), although it is very difficult to get
killed, Positive if the target block is touched (+2000) and negative if the
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
    id='MinecraftSimpleRoomMaze-v0',
    group='minecraft',
    summary='Simple room maze!',
    description="""
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
