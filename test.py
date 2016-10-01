import gym
import gym_pull
import tambetm_gym_minecraft

env = gym.make('tambetm/MinecraftBasic-v0')

for _ in xrange(2):
    env.reset()
    done = False
    while not done:
        obs, reward, done, info = env.step(env.action_space.sample())
        env.render()
        print "obs:", obs.shape
        print "reward:", reward
        print "done:", done
        print "info", info
