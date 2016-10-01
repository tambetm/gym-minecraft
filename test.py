import gym
import gym_pull
import tambetm_gym_minecraft
import time

env = gym.make('tambetm/MinecraftBasic-v0')
#env.configure(allowDiscreteMovement=True)
env.configure(videoResolution=[640, 480])

for _ in xrange(2):
    t = time.time()
    env.reset()
    t2 = time.time()
    print "Startup time:", t2 - t
    done = False
    s = 0
    while not done:
        obs, reward, done, info = env.step(env.action_space.sample())
        env.render()
        #print "obs:", obs.shape
        #print "reward:", reward
        #print "done:", done
        #print "info", info
        s += 1
    t3 = time.time()
    print "Time:", (t3 - t2), "Steps:", s, "Steps/s:", s / (t3 - t2)
