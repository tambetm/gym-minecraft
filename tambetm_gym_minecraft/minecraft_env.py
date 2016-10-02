import logging
import time
import os

import numpy as np
import gym
import gym.spaces
import MalmoPython

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MinecraftEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, mission_file):
        super(MinecraftEnv, self).__init__()

        # TODO: start Minecraft process?

        self.agent_host = MalmoPython.AgentHost()
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        mission_file = os.path.join(assets_dir, mission_file)
        logger.info("Loading mission from " + mission_file)
        mission_xml = open(mission_file, 'r').read()
        self.mission_spec = MalmoPython.MissionSpec(mission_xml, True)
        logger.info("Loaded mission: " + self.mission_spec.getSummary())

    def _configure(self, max_retries=3, step_sleep=0,
                   videoResolution=None, videoWithDepth=None,
                   observeRecentCommands=None, observeHotBar=None,
                   observeFullInventory=None, observeGrid=None,
                   observeDistance=None, observeChat=None,
                   allowContinuousMovement=None, allowDiscreteMovement=None,
                   allowAbsoluteMovement=None):

        self.max_retries = max_retries
        self.step_sleep = step_sleep

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

        if allowContinuousMovement or allowDiscreteMovement or allowAbsoluteMovement:
            # if there are any parameters, remove current command handlers first
            self.mission_spec.removeAllCommandHandlers()

            if allowContinuousMovement is True:
                self.mission_spec.allowAllContinuousMovementCommands()
            elif isinstance(allowContinuousMovement, list):
                for cmd in allowContinuousMovement:
                    self.mission_spec.allowContinuousMovementCommand(cmd)

            if allowDiscreteMovement is True:
                self.mission_spec.allowAllDiscreteMovementCommands()
            elif isinstance(allowDiscreteMovement, list):
                for cmd in allowDiscreteMovement:
                    self.mission_spec.allowDiscreteMovementCommand(cmd)

            if allowAbsoluteMovement is True:
                self.mission_spec.allowAllAbsoluteMovementCommands()
            elif isinstance(allowAbsoluteMovement, list):
                for cmd in allowAbsoluteMovement:
                    self.mission_spec.allowAbsoluteMovementCommand(cmd)

        # TODO: produce observation space dynamically based on requested features

        video_height = self.mission_spec.getVideoHeight(0)
        video_width = self.mission_spec.getVideoWidth(0)
        video_depth = self.mission_spec.getVideoChannels(0)
        self.observation_space = gym.spaces.Box(low=0, high=255,
                shape=(video_height, video_width, video_depth))
        # dummy image just for the first observation
        self.last_image = np.zeros((video_height, video_width, video_depth))

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
                        discrete_actions.append(cmd + " 1")
                    elif cmd in ["move", "turn", "look"]:
                        discrete_actions.append(cmd + " 1")
                        discrete_actions.append(cmd + " -1")
                    elif cmd in ["jump", "attack", "use"]:
                        discrete_actions.append(cmd + " 1")
                    else:
                        assert False, "Unknown discrete action " + cmd
                # TODO: support for AbsoluteMovement
                else:
                    assert False, "Unknown commandhandler " + ch

        # turn action lists into action spaces
        self.action_names = []
        self.action_spaces = []
        if len(discrete_actions) > 0:
            self.action_spaces.append(gym.spaces.Discrete(len(discrete_actions)))
            self.action_names.append(discrete_actions)
        if len(continuous_actions) > 0:
            self.action_spaces.append(gym.spaces.Box(-1, 1, (len(continuous_actions),)))
            self.action_names.append(continuous_actions)
        if len(multidiscrete_actions) > 0:
            self.action_spaces.append(gym.spaces.MultiDiscrete(multidiscrete_action_ranges))
            self.action_names.append(multidiscrete_actions)

        # if there is only one action space, don't wrap it in Tuple
        if len(self.action_spaces) == 1:
            self.action_space = self.action_spaces[0]
        else:
            self.action_space = gym.spaces.Tuple(self.action_spaces)
        logger.debug(self.action_space)

    def _reset(self):
        # Attempt to start a mission
        for retry in range(self.max_retries):
            try:
                self.agent_host.startMission(self.mission_spec, self.mission_record_spec)
                break
            except RuntimeError as e:
                if retry == self.max_retries - 1:
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
        return self._get_observation(world_state)

    def _take_action(self, actions):
        # if there is only one action space, it wasn't wrapped in Tuple
        if len(self.action_spaces) == 1:
            actions = [actions]

        # send appropriate command for different actions
        for spc, cmds, acts in zip(self.action_spaces, self.action_names, actions):
            if isinstance(spc, gym.spaces.Discrete):
                logger.debug(cmds[acts])
                self.agent_host.sendCommand(cmds[acts])
            elif isinstance(spc, gym.spaces.Box):
                for cmd, val in zip(cmds, acts):
                    logger.debug(cmd + " " + str(val))
                    self.agent_host.sendCommand(cmd + " " + str(val))
            elif isinstance(spc, gym.spaces.MultiDiscrete):
                for cmd, val in zip(cmds, acts):
                    logger.debug(cmd + " " + str(val))
                    self.agent_host.sendCommand(cmd + " " + str(val))

    def _get_world_state(self):
        # wait till we have got at least one video frame or mission has ended
        while True:
            time.sleep(self.step_sleep)  # TODO: how long this should be?
            world_state = self.agent_host.peekWorldState()
            if len(world_state.video_frames) > 0 or not world_state.is_mission_running:
                break

        return self.agent_host.getWorldState()

    def _get_observation(self, world_state):
        # process the video frame
        if len(world_state.video_frames) > 0:
            assert len(world_state.video_frames) == 1
            frame = world_state.video_frames[0]
            image = np.frombuffer(frame.pixels, dtype=np.uint8)
            image = image.reshape((frame.height, frame.width, frame.channels))
            #logger.debug(image)
            self.last_image = image
        else:
            # can happen only when mission ends before we get frame
            # then just use the last frame, it doesn't matter much anyway
            image = self.last_image

        return image

    def _step(self, action):
        # take the action only if mission is still running
        world_state = self.agent_host.peekWorldState()
        if world_state.is_mission_running:
            # take action
            self._take_action(action)
        # wait for the new state
        world_state = self._get_world_state()

        # log errors and control messages
        for error in world_state.errors:
            logger.warn(error.text)
        for msg in world_state.mission_control_messages:
            logger.info(msg.text)

        # sum rewards (actually there should be only one)
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()

        # take last frame from world state
        image = self._get_observation(world_state)

        # detect terminal state
        done = not world_state.is_mission_running

        # other auxiliary data
        info = {}
        info['has_mission_begun'] = world_state.has_mission_begun
        info['is_mission_running'] = world_state.is_mission_running
        info['number_of_video_frames_since_last_state'] = world_state.number_of_video_frames_since_last_state
        info['number_of_rewards_since_last_state'] = world_state.number_of_rewards_since_last_state
        info['number_of_observations_since_last_state'] = world_state.number_of_observations_since_last_state

        return image, reward, done, info

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
            assert False, "Unknown render mode: " + mode

    def _close(self):
        # TODO: shut down Minecraft process?
        pass

    def _seed(self, seed=None):
        self.mission_spec.setWorldSeed(seed)


class MinecraftDefaultWorld1Env(MinecraftEnv):
    def __init__(self):
        super(MinecraftDefaultWorld1Env, self).__init__("default_world_1.xml")


class MinecraftDefaultFlat1Env(MinecraftEnv):
    def __init__(self):
        super(MinecraftDefaultFlat1Env, self).__init__("default_flat_1.xml")


class MinecraftTrickyArena1Env(MinecraftEnv):
    def __init__(self):
        super(MinecraftTrickyArena1Env, self).__init__("tricky_arena_1.xml")


class MinecraftEating1Env(MinecraftEnv):
    def __init__(self):
        super(MinecraftEating1Env, self).__init__("eating_1.xml")


class MinecraftCliffWalking1Env(MinecraftEnv):
    def __init__(self):
        super(MinecraftCliffWalking1Env, self).__init__("cliff_walking_1.xml")


class MinecraftMaze1Env(MinecraftEnv):
    def __init__(self):
        super(MinecraftMaze1Env, self).__init__("maze_1.xml")


class MinecraftMaze2Env(MinecraftEnv):
    def __init__(self):
        super(MinecraftMaze2Env, self).__init__("maze_2.xml")


class MinecraftBasicEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftBasicEnv, self).__init__("basic.xml")


class MinecraftObstaclesEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftObstaclesEnv, self).__init__("obstacles.xml")


class MinecraftSimpleRoomMazeEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftSimpleRoomMazeEnv, self).__init__("simpleRoomMaze.xml")


class MinecraftAtticEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftAtticEnv, self).__init__("attic.xml")


class MinecraftVerticalEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftVerticalEnv, self).__init__("vertical.xml")


class MinecraftComplexityUsageEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftComplexityUsageEnv, self).__init__("complexity_usage.xml")


class MinecraftMediumEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftMediumEnv, self).__init__("medium.xml")


class MinecraftHardEnv(MinecraftEnv):
    def __init__(self):
        super(MinecraftHardEnv, self).__init__("hard.xml")
