import gym
import numpy as np

from gym_robot.envs.helper import constants
from gym_robot.envs.robot_world import RobotWorld
from gym_robot.envs.helper import Location, Square


class RobotEnv(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
        "obs.modes": ["grid", "image"]
    }
    visited = []
    action_meanings = dict(UP=1, DOWN=2, lEFT=3, RIGHT=4)
    action_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    action_space = gym.spaces.Discrete(len(action_meanings))

    def __init__(self, world_size=(9, 9), obs_mode="image"):
        self.world_size = world_size
        self.obs_mode = obs_mode
        self.eval_mode = False
        self.world = RobotWorld(size=world_size)

        self.observation_space = gym.spaces.Box(0, 255, shape=(*np.array(world_size) * constants.SIZE_SQUARE, 3))
        if obs_mode == "grid":
            self.observation_space = gym.spaces.Box(0, 3, shape=world_size)
            # low = np.zeros(len(self.world_size), dtype=int)
            # high =  np.array(self.world_size, dtype=int) - np.ones(len(self.world_size), dtype=int)
            # self.observation_space = gym.spaces.Box(low, high,  dtype=np.int64)

    def reset(self):
        self.world.reset()
        self.visited = []
        return self._get_obs(self.obs_mode)

    def set_eval(self):
        # print('Evaluation')
        self.eval_mode = True

    def set_train(self):
        # print('Training')
        self.eval_mode = False

    def render(self, mode="human", delay=1):
        if mode == 'human':
            return self.world.render(delay=delay)
        if mode == 'rgb_array':
            return self._get_obs(self.obs_mode)
        raise ValueError(f"Unknown mode {mode!r}, valid modes: {self.metadata['render.modes']}")

    def step(self, action: int):
        agent = self.world.agents[0]
        agent.add(self.action_directions[action])

        # Restore agent position if going out of bounds
        if not agent.in_bounds(self.world_size):
            agent.sub(self.action_directions[action])

        if agent in self.world.flag:
            return self._get_obs(self.obs_mode), 100, True, dict()

        # Restore agent position if going out of bounds or through buildings.
        if agent in self.world.immovable or not agent.in_bounds(self.world_size):
            agent.sub(self.action_directions[action])
            return self._get_obs(self.obs_mode), -1, False, dict()

        # Visited Nodes rendering
        if self.eval_mode:
            if not self.visited:  # append the initial position
                self.visited.append((0, 0))
            else:  # append all visited nodes
                if (agent.x, agent.y) not in self.visited:
                    self.visited.append((agent.x, agent.y))
            # Check if we need to update the world with the visited nodes
            for node in self.visited:
                if any(element.location.x == node[0] and element.location.y == node[1] and element.sprite_name == 'tree_1'
                       for element in self.world.world):
                    continue
                else:
                    self.world.world.append(Square(location=node, sprite_name='tree_1'))
            # pop the current node from the visited list to render the robot correctly
            for cnt, element in enumerate(self.world.world):
                if element.location.x == agent.x and element.location.y == agent.y and element.sprite_name == 'tree_1':
                    self.world.world.pop(cnt)
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
