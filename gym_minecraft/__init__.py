from gym.envs.registration import register
from gym.scoreboard.registration import add_task, add_group

# Env registration
# ==========================

register(
    id='MinecraftDefaultWorld1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'default_world_1.xml'}
)

register(
    id='MinecraftDefaultFlat1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'default_flat_1.xml'}
)

register(
    id='MinecraftTrickyArena1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'tricky_arena_1.xml'}
)

register(
    id='MinecraftEating1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'eating_1.xml'}
)

register(
    id='MinecraftCliffWalking1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'cliff_walking_1.xml'}
)

register(
    id='MinecraftMaze1-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'maze_1.xml'}
)

register(
    id='MinecraftMaze2-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'maze_2.xml'}
)

register(
    id='MinecraftBasic-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'basic.xml'}
)

register(
    id='MinecraftObstacles-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'obstacles.xml'}
)

register(
    id='MinecraftSimpleRoomMaze-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'simpleRoomMaze.xml'}
)

register(
    id='MinecraftAttic-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'attic.xml'}
)

register(
    id='MinecraftVertical-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'vertical.xml'}
)

register(
    id='MinecraftComplexityUsage-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'complexity_usage.xml'}
)

register(
    id='MinecraftMedium-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'medium.xml'}
)

register(
    id='MinecraftHard-v0',
    entry_point='gym_minecraft.envs:MinecraftEnv',
    kwargs={'mission_file': 'hard.xml'}
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
included Issue #73.
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
Task ends if target block is reached. Or if the timeLimitMs=20000 (30 sec.)
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
