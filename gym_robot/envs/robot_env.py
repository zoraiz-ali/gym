import gym
import numpy as np

from gym_robot.envs.helper import constants
from gym_robot.envs.robot_world import RobotWorld


class RobotEnv(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
        "obs.modes": ["grid", "image"]
    }

    action_meanings = dict(UP=1, DOWN=2, lEFT=3, RIGHT=4)
    action_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    action_space = gym.spaces.Discrete(len(action_meanings))

    def __init__(self, world_size=(9, 9), obs_mode="image"):
        self.world_size = world_size
        self.obs_mode = obs_mode

        self.world = RobotWorld(size=world_size)

        self.observation_space = gym.spaces.Box(0, 255, shape=(*np.array(world_size) * constants.SIZE_SQUARE, 3))
        if obs_mode == "grid":
            self.observation_space = gym.spaces.Box(0, 3, shape=world_size)

    def reset(self):
        self.world.reset()
        return self._get_obs(self.obs_mode)

    def render(self, mode="human", delay=1):
        if mode == 'human':
            return self.world.render(delay=delay)
        if mode == 'rgb_array':
            return self._get_obs(self.obs_mode)
        raise ValueError(f"Unknown mode {mode!r}, valid modes: {self.metadata['render.modes']}")

    def step(self, action: int):
        agent = self.world.agents[0]
        agent.add(self.action_directions[action])

        if agent in self.world.flag:
            return self._get_obs(self.obs_mode), 1, True, dict()

        # Restore agent position if going out of bounds or through buildings.
        if agent in self.world.immovable or not agent.in_bounds(self.world_size):
            agent.sub(self.action_directions[action])
            return self._get_obs(self.obs_mode), -1, False, dict()

        return self._get_obs(self.obs_mode), 0, False, dict()

    def _get_obs(self, mode='grid'):
        """
            Returns the observation from the world.

            :param str mode:
                This determines the size of the observation that should be returned.

                grid: return a world size grid with the values 0-4
                image: returns an image sized object (world size * constants.SIZE_SQUARE)

            Returns a smaller version of the world.
        """
        if mode == 'grid':
            return self.world.grid()
        if mode == 'image':
            return self.world.image()
        raise ValueError(f"Invalid observation mode {mode!r}, valid modes: {self.metadata['obs.modes']}")

    def close(self):
        self.world.close()
