# gym-minecraft

Gym Minecraft is an environment bundle for OpenAI Gym

## Prerequisites

First you need [Microsoft's Malmö](https://github.com/Microsoft/malmo), which is a platform for Artificial Intelligence experimentation and research built on top of Minecraft.

1. Install the dependencies for your OS: [Windows](https://github.com/Microsoft/malmo/blob/master/doc/install_windows.md), [Linux](https://github.com/Microsoft/malmo/blob/master/doc/install_linux.md), [MacOSX](https://github.com/Microsoft/malmo/blob/master/doc/install_macosx.md). You can skip Torch, Mono and ALE parts.

2. Download and unpack [the latest pre-built version for your OS](https://github.com/Microsoft/malmo/releases).

3. Set MALMO_XSD_PATH to the location of schemas, i.e. `export MALMO_XSD_PATH=$HOME/Malmo/Schemas`. Put this in your `~/.bashrc`.

4. Set PYTHONPATH to the location of MalmoPython.so, i.e. `export PYTHONPATH=$PYTHONPATH:$HOME/Malmo/Python_Examples`. Put this also in your `~/.bashrc`.

5. Launch Minecraft:
```shell
	cd ~/Malmo/Minecraft
	./launchClient.sh
```
You can leave Minecraft running for entire duration of your experiments. You also do not need to be in special menu in Minecraft, the Malmo mod switches the game mode automatically when it needs to.

6. Optional: in Minecraft go to Options..., Video Settings... and set Max Framerate: Unlimited. This allows to train faster.

## Installation

You need to install [gym-pull](https://github.com/ppaquette/gym-pull)

```shell
    pip install gym-pull
```

 To load and run the environments, run

```python
    import gym
	import gym_pull
	gym_pull.pull('github.com/tambetm/gym-minecraft')        # Only required once, envs will be loaded with import gym_pull afterwards
	env = gym.make('tambetm/MinecraftBasic-v0')
```

See test folder for some example scripts.

## Environments

Environments included:
- tambetm/MinecraftDefaultWorld1-v0
- tambetm/MinecraftDefaultFlat1-v0
- tambetm/MinecraftTrickyArena1-v0
- tambetm/MinecraftEating1-v0
- tambetm/MinecraftCliffWalking1-v0
- tambetm/MinecraftMaze1-v0
- tambetm/MinecraftMaze2-v0
- tambetm/MinecraftBasic-v0
- tambetm/MinecraftObstacles-v0
- tambetm/MinecraftSimpleRoomMaze-v0
- tambetm/MinecraftAttic-v0
- tambetm/MinecraftVertical-v0
- tambetm/MinecraftComplexityUsage-v0
- tambetm/MinecraftMedium-v0
- tambetm/MinecraftHard-v0

Basically I used original Malmö missions intact, only added `<PrioritiseOffscreenRendering>` tag to speed up training.

## Overriding default settings

The default settings for environments might not be optimal for you. Luckily you can easily override them using configure().

For example to use discrete actions instead of continuous actions:

```python
	env = gym.make('tambetm/MinecraftBasic-v0')
	env.configure(allowDiscreteMovement=["move", "turn"])
```

To use continuous actions instead of discrete actions:

```python
	env = gym.make('tambetm/MinecraftBasic-v0')
	env.configure(allowContinuousMovement=["move", "turn"])
```

To use different video resolution:

```python
	env = gym.make('tambetm/MinecraftBasic-v0')
	env.configure(videoResolution=[40, 30])
```

More documentation about configuration options is coming, meanwhile refer to the source code.
