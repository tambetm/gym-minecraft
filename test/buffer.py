import numpy as np


class Buffer:
    def __init__(self, size, observation_shape, action_shape, observation_dtype=np.float, action_dtype=np.integer, reward_dtype=np.float):
        self.size = size
        self.observation_shape = observation_shape
        self.action_shape = action_shape

        self.preobs = np.empty((self.size,) + observation_shape, dtype=observation_dtype)
        self.actions = np.empty((self.size,) + action_shape, dtype=action_dtype)
        self.rewards = np.empty(self.size, dtype=reward_dtype)
        self.postobs = np.empty((self.size,) + observation_shape, dtype=observation_dtype)
        self.terminals = np.empty(self.size, dtype=np.bool)

        self.count = 0
        self.current = 0

    def add(self, preobs, action, reward, postobs, terminal):
        assert preobs.shape == self.observation_shape
        assert action.shape == self.action_shape
        assert postobs.shape == self.observation_shape
        self.preobs[self.current] = preobs
        self.actions[self.current] = action
        self.rewards[self.current] = reward
        self.postobs[self.current] = postobs
        self.terminals[self.current] = terminal
        self.count = max(self.count, self.current + 1)
        self.current = (self.current + 1) % self.size

    def addBatch(self, preobs, actions, rewards, postobs, terminals):
        for preob, action, reward, postob, terminal in zip(preobs, actions, rewards, postobs, terminals):
            self.add(preob, action, reward, postob, terminal)

    def sample(self, batch_size):
        assert self.count > 0
        indexes = np.random.choice(self.count, size=batch_size)
        return self.preobs[indexes], self.actions[indexes], self.rewards[indexes], self.postobs[indexes], self.terminals[indexes]
