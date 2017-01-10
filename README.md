# Gym Minecraft

Gym Minecraft is an environment bundle for OpenAI Gym. It is based on [Microsoft's Malmö](https://github.com/Microsoft/malmo), which is a platform for Artificial Intelligence experimentation and research built on top of Minecraft.

<table>
<tr>
<td>
MinecraftDefaultWorld1-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftDefaultWorld1-v0.png" width="280" height="210" />
</td>
<td>
MinecraftDefaultFlat1-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftDefaultFlat1-v0.png" width="280" height="210"/>
</td>
<td>
MinecraftTrickyArena1-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftTrickyArena1-v0.png" width="280" height="210"/>
</td>
</tr>
<tr>
<td>
MinecraftEating1-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftEating1-v0.png" width="280" height="210" />
</td>
<td>
MinecraftCliffWalking1-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftCliffWalking1-v0.png" width="280" height="210"/>
</td>
<td>
MinecraftMaze1-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftMaze1-v0.png" width="280" height="210"/>
</td>
</tr>
<tr>
<td>
MinecraftMaze2-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftMaze2-v0.png" width="280" height="210" />
</td>
<td>
MinecraftBasic-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftBasic-v0.png" width="280" height="210"/>
</td>
<td>
MinecraftObstacles-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftObstacles-v0.png" width="280" height="210"/>
</td>
</tr>
<tr>
<td>
MinecraftSimpleRoomMaze-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftSimpleRoomMaze-v0.png" width="280" height="210" />
</td>
<td>
MinecraftAttic-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftAttic-v0.png" width="280" height="210"/>
</td>
<td>
MinecraftVertical-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftVertical-v0.png" width="280" height="210"/>
</td>
</tr>
<tr>
<td>
MinecraftComplexityUsage-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftComplexityUsage-v0.png" width="280" height="210" />
</td>
<td>
MinecraftMedium-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftMedium-v0.png" width="280" height="210"/>
</td>
<td>
MinecraftHard-v0<br/>
<img src="https://raw.githubusercontent.com/tambetm/gym-minecraft/master/images/MinecraftHard-v0.png" width="280" height="210"/>
</td>
</tr>
</table>

Basically these are [original Malmö missions](https://github.com/Microsoft/malmo/raw/master/sample_missions/MalmoMissionTable_CurrentTasks_2016_06_14.pdf) with only `<PrioritiseOffscreenRendering>` added to speed up training.

## Installation

1. Install the dependencies for your OS: [Windows](https://github.com/Microsoft/malmo/blob/master/doc/install_windows.md), [Linux](https://github.com/Microsoft/malmo/blob/master/doc/install_linux.md), [MacOSX](https://github.com/Microsoft/malmo/blob/master/doc/install_macosx.md). You can skip Torch, Mono and ALE parts.

2. Install [OpenAI Gym](https://github.com/openai/gym) and its dependencies.
 ```
pip install gym
```

3. Download and install [minecraft_py](https://github.com/tambetm/minecraft-py).
 ```
git clone https://github.com/tambetm/minecraft-py.git
cd minecraft-py
# NB! `minecraft_py` should be installed to writable user directory, either in virtualenv or with `--user` option.
python setup.py install
```

4. Download and install `gym-minecraft`:

 ```
git clone https://github.com/tambetm/gym-minecraft.git
cd gym-minecraft
python setup.py install
```

 `gym-minecraft` needs `pygame` to render Minecraft screen. It is best to have pygame installed via your system commands, i.e. `sudo apt-get install python-pygame` or `conda install pygame`. Otherwise setup will automatically download and compile `pygame`. This might need some additional dependencies though, see instructions for [Ubuntu](http://www.pygame.org/wiki/CompileUbuntu), [OSX](http://pygame.org/wiki/MacCompile) or [Windows](http://pygame.org/wiki/CompileWindows).

5. Run once following snippet:
 ```
import logging
logging.basicConfig(level=logging.DEBUG)

import minecraft_py

proc, port = minecraft_py.start()
minecraft_py.stop(proc)
```
 Basically Minecraft downloads and compiles everything on first start, this snippet just starts `minecraft_py` in debug mode, so you can see when Minecraft gets stuck.

## Running

```python
import gym
import gym_minecraft

env = gym.make('MinecraftBasic-v0')
env.init(start_minecraft=True)
env.reset()

done = False
while not done:
        env.render()
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)

env.close()
```

NB! Running Minecraft for the first time might take a while as it downloads and compiles itself. Next time the startup time should be shorter, but still around 30 seconds. In active development phase you might want to start one permanent Minecraft process in background and remove `start_minecraft=True`, see [wiki](https://github.com/tambetm/gym-minecraft/wiki/Parallel).

## Overriding default settings

The default settings for environments might not be optimal for you. Luckily you can easily override them using `init()`.

For example to use discrete actions instead of continuous actions:

```python
env = gym.make('MinecraftBasic-v0')
env.init(allowDiscreteMovement=["move", "turn"])
```

To use continuous actions instead of discrete actions:

```python
env = gym.make('MinecraftBasic-v0')
env.init(allowContinuousMovement=["move", "turn"])
```

To use different video resolution:

```python
env = gym.make('MinecraftBasic-v0')
env.init(videoResolution=[40, 30])
```

More documentation about configuration options is in [wiki](https://github.com/tambetm/gym-minecraft/wiki/Configure).
