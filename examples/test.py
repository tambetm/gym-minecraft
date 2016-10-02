import gym
import gym_minecraft
import time

env = gym.make('MinecraftBasic-v0')
#env.configure(allowContinuousMovement=["move", "turn"])
env.configure(allowDiscreteMovement=["move", "turn"], log_level="INFO")
#env.configure(videoResolution=[160, 120])
#env.monitor.start("gym_random")

for _ in xrange(10):
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
    print (t3 - t2), "seconds total,", s, "steps total,", s / (t3 - t2), "steps/second"

#env.monitor.close()
