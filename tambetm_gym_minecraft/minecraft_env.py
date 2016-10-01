import logging
import time
import os

# import multiprocessing

import numpy as np

import gym
from gym import spaces, error
# from gym.utils import seeding

import MalmoPython

'''
try:
    import MalmoPython
except ImportError as e:
    raise gym.error.DependencyNotInstalled("{}. (HINT: your PYTHONPATH should include MalmoPython.so.)'".format(e))
'''

logger = logging.getLogger(__name__)

'''
# Singleton pattern
class MinecraftLock:
    lock = None
    def __init__(self):
        if not MinecraftLock.lock:
            MinecraftLock.lock = multiprocessing.Lock()
    def get_lock(self):
        return MinecraftLock.lock
'''


class MinecraftEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, mission_file):
        super(MinecraftEnv, self).__init__()

        # TODO: start Minecraft process

        self.agent_host = MalmoPython.AgentHost()
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        mission_file = os.path.join(assets_dir, mission_file)
        logger.info("Loading mission from " + mission_file)
        mission_xml = open(mission_file, 'r').read()
        self.mission_spec = MalmoPython.MissionSpec(mission_xml, True)

        self._configure()

    def _configure(self, videoResolution=None, videoWithDepth=None,
                   observeRecentCommands=None, observeHotBar=None,
                   observeFullInventory=None, observeGrid=None,
                   observeDistance=None, observeChat=None,
                   allowContinuousMovement=None, allowDiscreteMovement=None,
                   allowAbsoluteMovement=None):

        if videoResolution:
            if videoWithDepth:
                self.mission_spec.requestVideoWithDepth(*videoResolution)
            else:
                self.mission_spec.requestVideo(*videoResolution)

        if observeRecentCommands:
            self.mission_spec.observeRecentCommands()
        if observeHotBar:
            self.mission_spec.observeHotBar()
        if observeFullInventory:
            self.mission_spec.observeFullInventory()
        if observeGrid:
            self.mission_spec.observeGrid(*(observeGrid + ["grid"]))
        if observeDistance:
            self.mission_spec.observeDistance(*(observeDistance + ["dist"]))
        if observeChat:
            self.mission_spec.observeChat()

        if allowContinuousMovement:
            self.mission_spec.allowContinuousMovement()
        if allowDiscreteMovement:
            self.mission_spec.allowDiscreteMovement()
        if allowAbsoluteMovement:
            self.mission_spec.allowAbsoluteMovement()

        chs = self.mission_spec.getListOfCommandHandlers(0)
        logger.debug(chs)
        for ch in chs:
            cmds = self.mission_spec.getAllowedCommands(0, ch)
            logger.debug(ch+':'+str(cmds))

        # TODO: produce observation and action spaces dynamically based on
        # requested features

        video_height = self.mission_spec.getVideoHeight(0)
        video_width = self.mission_spec.getVideoWidth(0)
        video_depth = self.mission_spec.getVideoChannels(0)
        self.observation_space = spaces.Box(low=0, high=255, 
                shape=(video_depth, video_width, video_height))
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,))  # move and turn

        # TODO: allow configuration of MissionRecordSpec
        self.mission_record_spec = MalmoPython.MissionRecordSpec()  # record nothing

    def _reset(self):
        # Attempt to start a mission
        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agent_host.startMission(self.mission_spec, self.mission_record_spec)
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    logger.error("Error starting mission: "+str(e))
                    raise
                else:
                    logger.warn("Error starting mission: "+str(e))
                    time.sleep(2)

        # Loop until mission starts:
        logger.info("Waiting for the mission to start")
        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                logger.warn(error.text)

        logger.info("Mission running")

    def _step(self, action):
        assert action.shape == (2,)
        assert np.all(-1 <= action)
        assert np.all(action <= 1)

        world_state = self.agent_host.peekWorldState()
        assert world_state.is_mission_running

        try:
            # TODO: support other commands besides these two
            self.agent_host.sendCommand("move "+str(action[0]))
            self.agent_host.sendCommand("turn "+str(action[1]))
            time.sleep(0.05)  # TODO: how long this should be?
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                logger.warn(error.text)

            for msg in world_state.mission_control_messages:
                logger.debug(msg)

            assert len(world_state.video_frames) == 1
            # assert len(world_state.rewards) == 1
            # assert len(world_state.observations) == 1
            frame = world_state.video_frames[0]
            image = np.frombuffer(frame.pixels, dtype=np.uint8)
            image = image.reshape((frame.height, frame.width, frame.channels))            

            reward = 0
            for r in world_state.rewards:
                reward += r.getValue()
            done = not world_state.is_mission_running

            info = {}
            info['has_mission_begun'] = world_state.has_mission_begun
            info['is_mission_running'] = world_state.is_mission_running
            info['number_of_video_frames_since_last_state'] = world_state.number_of_video_frames_since_last_state
            info['number_of_rewards_since_last_state'] = world_state.number_of_rewards_since_last_state
            info['number_of_observations_since_last_state'] = world_state.number_of_observations_since_last_state

            logger.debug(image)
            self.last_image = image
            # TODO: return other observations besides video frame
            return image, reward, done, info

        except RuntimeError as e:
            logger.warn("Failed to send command: " + str(e))

    def _render(self, mode='human', close=False):
        if mode == 'rgb_array':
            return self.last_image
        elif mode == 'human':
            import cv2
            if close:
                cv2.destroyAllWindows()
            else:
                cv2.imshow('render', self.last_image[...,::-1])  # OpenCV expects images in BGR
                cv2.waitKey(1)
        else:
            assert False, "Unknown render mode " + mode

    def _close(self):
        # TODO: shut down Minecraft process
        pass

    def _seed(self, seed=None):
        self.mission_spec.setWorldSeed(seed)


class MinecraftBasicEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftBasicEnv, self).__init__("basic.xml")
