# gym-minecraft
#### **Gym Minecraft is an environment bundle for OpenAI Gym**
---
<div id="installation"></div>Installation
============

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

Environments included:
============
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
