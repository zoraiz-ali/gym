import gym
import numpy as np

from gym_robot.envs.helper import constants
from gym_robot.envs.robot_world import RobotWorld


class RobotEnv(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
    }

    action_meanings = dict(NOOP=0, UP=1, DOWN=2, lEFT=3, RIGHT=4)
    action_directions = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]

    action_space = gym.spaces.Discrete(len(action_meanings))

    def __init__(self, world_size=(9, 9)):
        self.world_size = world_size
        self.world = RobotWorld(size=world_size)
        self.observation_space = gym.spaces.Box(0, 255, shape=np.array(world_size) * constants.SIZE_SQUARE)

    def reset(self):
        self.world.reset()
        return self.world.image()

    def render(self, mode="human", delay=1):
        if mode == 'human':
            return self.world.render(delay=delay)
        if mode == 'rgb_array':
            return self.world.image()
        raise ValueError(f"Unknown mode {mode!r}, valid modes: {self.metadata['render.modes']}")

    def step(self, action: int):
        agent = self.world.agents[0]
        agent.add(self.action_directions[action])

        # Restore agent position if going out of bounds
        if not agent.in_bounds(self.world_size):
            agent.sub(self.action_directions[action])

        if agent in self.world.flag:
            return self.world.image(), 1, True, dict()

        if agent in self.world.immovable or not agent.in_bounds(self.world_size):
            return self.world.image(), -1, True, dict()

        return self.world.image(), 0, False, dict()

    def close(self):
        self.world.close()
