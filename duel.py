import argparse
import gym
import gym_pull
import tambetm_gym_minecraft
from gym.spaces import Box, Discrete
from keras.models import Model
from keras.layers import Input, Permute, Convolution2D, Flatten, Dense, Lambda
from keras import backend as K
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--hidden_size', type=int, default=256)
parser.add_argument('--layers', type=int, default=1)
parser.add_argument('--min_train', type=int, default=10)
parser.add_argument('--train_repeat', type=int, default=10)
parser.add_argument('--gamma', type=float, default=0.99)
parser.add_argument('--tau', type=float, default=0.001)
parser.add_argument('--episodes', type=int, default=200)
parser.add_argument('--max_timesteps', type=int, default=200)
parser.add_argument('--activation', choices=['tanh', 'relu'], default='relu')
parser.add_argument('--optimizer', choices=['adam', 'rmsprop'], default='adam')
#parser.add_argument('--optimizer_lr', type=float, default=0.001)
parser.add_argument('--exploration', type=float, default=0.1)
parser.add_argument('--advantage', choices=['naive', 'max', 'avg'], default='naive')
parser.add_argument('--display', action='store_true', default=True)
parser.add_argument('--no_display', dest='display', action='store_false')
parser.add_argument('--gym_record')
parser.add_argument('environment')
args = parser.parse_args()

env = gym.make(args.environment)
env.configure(videoResolution=[40, 30], allowDiscreteMovement=["move", "turn"])
assert isinstance(env.observation_space, Box)
assert isinstance(env.action_space, Discrete)

if args.gym_record:
    env.monitor.start(args.gym_record)


def createLayers():
    x = Input(shape=env.observation_space.shape)
    h = Permute((3, 1, 2))(x)
    h = Convolution2D(32, 4, 4, subsample=(2, 2), activation=args.activation)(h)
    h = Convolution2D(64, 4, 4, subsample=(2, 2), activation=args.activation)(h)
    h = Flatten()(h)
    for i in xrange(args.layers):
        h = Dense(args.hidden_size, activation=args.activation)(h)
    y = Dense(env.action_space.n + 1)(h)
    if args.advantage == 'avg':
        z = Lambda(lambda a: K.expand_dims(a[:, 0], dim=-1) + a[:, 1:] - K.mean(a[:, 1:], keepdims=True), output_shape=(env.action_space.n,))(y)
    elif args.advantage == 'max':
        z = Lambda(lambda a: K.expand_dims(a[:, 0], dim=-1) + a[:, 1:] - K.max(a[:, 1:], keepdims=True), output_shape=(env.action_space.n,))(y)
    elif args.advantage == 'naive':
        z = Lambda(lambda a: K.expand_dims(a[:, 0], dim=-1) + a[:, 1:], output_shape=(env.action_space.n,))(y)
    else:
        assert False

    return x, z

x, z = createLayers()
model = Model(input=x, output=z)
model.summary()
model.compile(optimizer=args.optimizer, loss='mse')

x, z = createLayers()
target_model = Model(input=x, output=z)
target_model.set_weights(model.get_weights())

prestates = []
actions = []
rewards = []
poststates = []
terminals = []

total_reward = 0
for i_episode in xrange(args.episodes):
    observation = env.reset()
    episode_reward = 0
    for t in xrange(args.max_timesteps):
        if args.display:
            env.render()

        if np.random.random() < args.exploration:
            action = env.action_space.sample()
        else:
            s = np.array([observation])
            q = model.predict(s, batch_size=1)
            #print "q:", q
            action = np.argmax(q[0])
        #print "action:", action

        prestates.append(observation)
        actions.append(action)

        observation, reward, done, info = env.step(action)
        episode_reward += reward
        #print "reward:", reward

        rewards.append(reward)
        poststates.append(observation)
        terminals.append(done)

        if len(prestates) > args.min_train:
            for k in xrange(args.train_repeat):
                if len(prestates) > args.batch_size:
                    indexes = np.random.choice(len(prestates), size=args.batch_size)
                else:
                    indexes = range(len(prestates))

                qpre = model.predict(np.array(prestates)[indexes])
                qpost = model.predict(np.array(poststates)[indexes])
                for i in xrange(len(indexes)):
                    if terminals[indexes[i]]:
                        qpre[i, actions[indexes[i]]] = rewards[indexes[i]]
                    else:
                        qpre[i, actions[indexes[i]]] = rewards[indexes[i]] + args.gamma * np.amax(qpost[i])
                model.train_on_batch(np.array(prestates)[indexes], qpre)

                weights = model.get_weights()
                target_weights = target_model.get_weights()
                for i in xrange(len(weights)):
                    target_weights[i] = args.tau * weights[i] + (1 - args.tau) * target_weights[i]
                target_model.set_weights(target_weights)

        if done:
            break

    print "Episode {} finished after {} timesteps, episode reward {}".format(i_episode + 1, t + 1, episode_reward)
    total_reward += episode_reward

print "Average reward per episode {}".format(total_reward / args.episodes)

if args.gym_record:
    env.monitor.close()
