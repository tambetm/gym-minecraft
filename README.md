# Gym Minecraft

Gym Minecraft is an environment bundle for OpenAI Gym. It is based on [Microsoft's Malmö](https://github.com/Microsoft/malmo), which is a platform for Artificial Intelligence experimentation and research built on top of Minecraft.

## Prerequisites

1. Install the dependencies for your OS: [Windows](https://github.com/Microsoft/malmo/blob/master/doc/install_windows.md), [Linux](https://github.com/Microsoft/malmo/blob/master/doc/install_linux.md), [MacOSX](https://github.com/Microsoft/malmo/blob/master/doc/install_macosx.md). You can skip Torch, Mono and ALE parts.

2. Download and unpack [the latest pre-built version for your OS](https://github.com/Microsoft/malmo/releases).

3. Set `MALMO_XSD_PATH` to the location of schemas, i.e. 
  ```shell
export MALMO_XSD_PATH=$HOME/Malmo/Schemas
```

4. Set `PYTHONPATH` to the location of `MalmoPython.so`, i.e.
  ```shell
export PYTHONPATH=$PYTHONPATH:$HOME/Malmo/Python_Examples
```

You can put the last two lines in your `~/.bashrc`.

## Installation

```shell
git clone https://github.com/tambetm/gym-minecraft.git
cd gym-minecraft
pip install -e .
```

## Running

1. Launch Minecraft:
  ```shell
cd ~/Malmo/Minecraft
./launchClient.sh
```
You can leave Minecraft running for entire duration of your experiments. You also do not need to be in special menu in Minecraft, the Malmo mod switches the game mode automatically when it needs to.

2. Run environment:

  ```python
import gym
import gym_minecraft

env = gym.make('MinecraftBasic-v0')
...
```

See `examples` folder for sample scripts.

## Environments

Environments included:
- MinecraftDefaultWorld1-v0
- MinecraftDefaultFlat1-v0
- MinecraftTrickyArena1-v0
- MinecraftEating1-v0
- MinecraftCliffWalking1-v0
- MinecraftMaze1-v0
- MinecraftMaze2-v0
- MinecraftBasic-v0
- MinecraftObstacles-v0
- MinecraftSimpleRoomMaze-v0
- MinecraftAttic-v0
- MinecraftVertical-v0
- MinecraftComplexityUsage-v0
- MinecraftMedium-v0
- MinecraftHard-v0

Basically these are [original Malmö missions](https://github.com/Microsoft/malmo/raw/master/sample_missions/MalmoMissionTable_CurrentTasks_2016_06_14.pdf) with only `<PrioritiseOffscreenRendering>` added to speed up training.

## Overriding default settings

The default settings for environments might not be optimal for you. Luckily you can easily override them using `configure()`.

For example to use discrete actions instead of continuous actions:

```python
env = gym.make('MinecraftBasic-v0')
env.configure(allowDiscreteMovement=["move", "turn"])
```

To use continuous actions instead of discrete actions:

```python
env = gym.make('MinecraftBasic-v0')
env.configure(allowContinuousMovement=["move", "turn"])
```

To use different video resolution:

```python
env = gym.make('MinecraftBasic-v0')
env.configure(videoResolution=[40, 30])
```

More documentation about configuration options is coming, meanwhile refer to the source code.

## Tuning the speed

Following optimizations help to run the training process faster: 

1. Turn up the framerate: in Minecraft go to `Options...`, `Video Settings...` and set `Max Framerate: Unlimited`.

2. Make sure you have offscreen rendering enabled in mission XML file (should be for default missions).

  ```xml
  <ModSettings>
      <PrioritiseOffscreenRendering>true</PrioritiseOffscreenRendering>
  </ModSettings>
```

3. You can play with `MsPerTick` parameter, which basically determines how fast you can get new observations from the game. Default is 50ms per tick, which means 20 observations per second. You can lower it to 25ms, 10ms or even 1ms. But beware that the bottleneck might be your training process - can it really handle more than 20 observations per second? Otherwise you would be wasting observations and moving forward in time in bigger steps (which might actually be good thing in some contexts).

  ```xml
  <ModSettings>
      <MsPerTick>10</MsPerTick>
  </ModSettings>
```
