import gym
import gym_minecraft

env = gym.make('MinecraftBasic-v0')
env.configure(client_pool=[("localhost", 10000), ("localhost", 10001), ("localhost", 10002)])
env.reset()

done = False
while not done:
    env.render()
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
