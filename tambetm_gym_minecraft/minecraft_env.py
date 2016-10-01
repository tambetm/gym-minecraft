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
logger.setLevel(logging.DEBUG)

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
        logger.info("Loaded mission: " + self.mission_spec.getSummary())

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
            self.mission_spec.allowAllContinuousMovementCommands()
        if allowDiscreteMovement:
            self.mission_spec.allowAllDiscreteMovementCommands()
        if allowAbsoluteMovement:
            self.mission_spec.allowAllAbsoluteMovementCommands()

        # TODO: produce observation space dynamically based on
        # requested features

        video_height = self.mission_spec.getVideoHeight(0)
        video_width = self.mission_spec.getVideoWidth(0)
        video_depth = self.mission_spec.getVideoChannels(0)
        self.observation_space = spaces.Box(low=0, high=255, 
                shape=(video_depth, video_width, video_height))

        self._create_action_space()

        # TODO: allow configuration of MissionRecordSpec
        self.mission_record_spec = MalmoPython.MissionRecordSpec()  # record nothing

    def _create_action_space(self):
        # collect different actions based on allowed commands
        continuous_actions = []
        discrete_actions = []
        multidiscrete_actions = []
        multidiscrete_action_ranges = []
        chs = self.mission_spec.getListOfCommandHandlers(0)
        for ch in chs:
            cmds = self.mission_spec.getAllowedCommands(0, ch)
            for cmd in cmds:
                logger.debug(ch + ":" + cmd)
                if ch == "ContinuousMovement":
                    if cmd in ["move", "strafe", "pitch", "turn"]:
                        continuous_actions.append(cmd)
                    elif cmd in ["crouch", "jump", "attack", "use"]:
                        multidiscrete_actions.append(cmd)
                        multidiscrete_action_ranges.append([0, 1])
                    else:
                        assert False, "Unknown continuous action " + cmd
                elif ch == "DiscreteMovement":
                    if cmd in ["movenorth", "moveeast", "movesouth", "movewest"]:
                        discrete_actions.append(cmd)
                    elif cmd in ["move", "turn", "look"]:
                        multidiscrete_actions.append(cmd)
                        multidiscrete_action_ranges.append([-1, 1])
                    elif cmd in ["jump", "attack", "use"]:
                        if cmd not in discrete_actions:
                            multidiscrete_actions.append(cmd)
                            multidiscrete_action_ranges.append([0, 1])
                    else:
                        assert False, "Unknown discrete action " + cmd
                # TODO: support for AbsoluteMovement
                else:
                    assert False, "Unknown commandhandler " + ch

        # turn action lists into action spaces
        self.action_names = []
        self.action_spaces = []
        if len(discrete_actions) > 0:
            self.action_spaces.append(spaces.Discrete(len(discrete_actions)))
            self.action_names.append(discrete_actions)
        if len(continuous_actions) > 0:
            self.action_spaces.append(spaces.Box(-1, 1, (len(continuous_actions),)))
            self.action_names.append(continuous_actions)
        if len(multidiscrete_actions) > 0:
            self.action_spaces.append(spaces.MultiDiscrete(multidiscrete_action_ranges))
            self.action_names.append(multidiscrete_actions)

        # if there is only one action space, don't wrap it in Tuple
        if len(self.action_spaces) == 1:
            self.action_space = self.action_spaces[0]
        else:
            self.action_space = spaces.Tuple(self.action_spaces)
        logger.debug(self.action_space)

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

    def _take_action(self, actions):
        # if there is only one action space, it wasn't wrapped in Tuple
        if len(self.action_spaces) == 1:
            actions = [actions]

        # send appropriate command for different actions
        for asp, cmds, acts in zip(self.action_spaces, self.action_names, actions):
            if isinstance(asp, spaces.Discrete):
                logger.debug(cmds[acts] + " 1")
                self.agent_host.sendCommand(cmds[acts] + " 1")
            elif isinstance(asp, spaces.Box):
                for cmd, val in zip(cmds, acts):
                    logger.debug(cmd + " " + str(val))
                    self.agent_host.sendCommand(cmd + " " + str(val))
            elif isinstance(asp, spaces.MultiDiscrete):
                for cmd, val in zip(cmds, acts):
                    logger.debug(cmd + " " + str(val))
                    self.agent_host.sendCommand(cmd + " " + str(val))

    def _get_state(self):
        reward = 0
        while True:
            time.sleep(0.01)  # TODO: how long this should be?
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                logger.warn(error.text)
            for msg in world_state.mission_control_messages:
                logger.info(msg.text)
            for r in world_state.rewards:
                reward += r.getValue()
            # if got at least video frame and mission hasn't ended
            if len(world_state.video_frames) > 0 or not world_state.is_mission_running:
                break

        if len(world_state.video_frames) > 0:
            assert len(world_state.video_frames) == 1
            # assert len(world_state.rewards) == 1
            # assert len(world_state.observations) == 1
            frame = world_state.video_frames[0]
            image = np.frombuffer(frame.pixels, dtype=np.uint8)
            image = image.reshape((frame.height, frame.width, frame.channels))
            #logger.debug(image)
            self.last_image = image
        else:
            # can happen only when mission ends before we get frame
            # then just use the last frame, it doesn't matter much anyway
            image = self.last_image

        done = not world_state.is_mission_running

        info = {}
        info['has_mission_begun'] = world_state.has_mission_begun
        info['is_mission_running'] = world_state.is_mission_running
        info['number_of_video_frames_since_last_state'] = world_state.number_of_video_frames_since_last_state
        info['number_of_rewards_since_last_state'] = world_state.number_of_rewards_since_last_state
        info['number_of_observations_since_last_state'] = world_state.number_of_observations_since_last_state

        return image, reward, done, info

    def _step(self, action):
        # you shouldn't call step() when previous step returned done=True
        world_state = self.agent_host.peekWorldState()
        assert world_state.is_mission_running, "You shouldn't call step() when previous step returned done=True."

        # take action and return new state
        self._take_action(action)
        return self._get_state()

    def _render(self, mode='human', close=False):
        if mode == 'rgb_array':
            return self.last_image
        elif mode == 'human':
            import cv2
            if close:
                cv2.destroyAllWindows()
            else:
                # OpenCV expects images in BGR
                image = self.last_image[..., ::-1]
                cv2.imshow('render', image)
                cv2.waitKey(1)  # wait the smallest amount possible - 1ms
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
