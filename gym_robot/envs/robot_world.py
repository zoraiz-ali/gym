import cv2
import numpy as np

#from typing import Tuple, Dict, List

#from gym_robot.envs.helper import constants, Size, Location, Square
from typing import Dict, Tuple

CAPTION = 'Deep Q-learning. Zoraiz Ali'

WORLD_SIZE = (9, 9)
SIZE_SQUARE = 40
FPS = 30

MAP: Dict[Tuple[int, int], str] = {
    (0, 0): 'agent_1', (0, 1): 'building_2', (0, 5): 'bank_2', (0, 8): 'tree_2',
    (1, 7): 'shop',
    (2, 0): 'road_closed_2', (2, 3): 'tree_1',
    (3, 2): 'tree_1', (3, 5): 'road_closed_3', (3, 7): 'pedestrian', (3, 8): 'traffic_lights',
    (4, 0): 'road_closed_1', (4, 3): 'tree_1',
    (5, 5): 'building_1', (5, 6): 'building_1', (5, 7): 'building_1',
    (6, 1): 'bank_1', (6, 5): 'building_1', (6, 6): 'flag', (6, 7): 'building_1',
    (7, 3): 'traffic_lights', (7, 5): 'building_1', (7, 7): 'building_1',
    (8, 0): 'tree_2',
}

import os
import numpy as np

import pyglet

from typing import Tuple
from pathlib import Path
from dataclasses import dataclass
from PIL import Image

#from gym_robot.envs.helper import constants


@dataclass
class Location:
    x: int
    y: int

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    def add(self, other: Tuple[int, int]):
        self.x += other[0]
        self.y += other[1]
        
    def sub(self, other: Tuple[int, int]):
        self.x -= other[0]
        self.y -= other[1]

    def in_bounds(self, world_size):
        return all(0 <= val < size for val, size in zip(self, world_size))


@dataclass
class Size:
    width: int
    height: int


class Square:
    """
        This stores the position, sprite name and an image of the sprite at
        a specific location on a 2D grid world.

        :param Tuple[int, int] location:
            This is the x and y position of the square

        :param str sprite_name:
            This is the name of the sprite that has to be loaded and the
            sprite should be located in the `images` folder, which should
            be located at the same level as this file.
    """

    def __init__(self, location: Tuple[int, int], sprite_name: str):
        self.location: Location = Location(*location)
        self.sprite_name: str = sprite_name
        self.image: np.ndarray = self._load_image(mode='np.array')
        self.sprite: pyglet.sprite.Sprite = self._load_image(mode='pyglet.sprite')

    def __repr__(self):
        return f"<class {type(self).__qualname__}, (location={self.location}, sprite={self.sprite_name!r})>"

    @property
    def x(self):
        return self.location.x * constants.SIZE_SQUARE

    @property
    def y(self):
        return self.location.y * constants.SIZE_SQUARE

    def _locate_image(self, path=None) -> str:
        """ Locate the image based on the path, or a default path. Returns the full path name.  """
        path = path if path is not None else os.path.join(Path(__file__).parents[1], 'images')
        valid_sprites = []
        for file in os.listdir(path):
            if Path(file).stem == self.sprite_name:
                return os.path.join(path, file)
            valid_sprites.append(Path(file).stem)
        raise ValueError(f"Sprite {self.sprite_name!r} is not known, valid sprites: {valid_sprites}")

    def _load_image(self, mode='np.array'):
        """
            Loads an image in a specified type, valid types are:

            pil.image:
                returns the image as a PIL Image
            np.array:
                Returns the image as a numpy array using PIL images
            pyglet.sprite:
                Returns
        """
        valid_types = {
            'pil.image': [Image.open],
            'np.array': [Image.open, np.array],
            'pyglet.sprite': [pyglet.image.load, (pyglet.sprite.Sprite, dict(x=self.x, y=self.y))]
        }

        if mode.lower() not in valid_types:
            raise ValueError(f"Type {mode!r} not recognized, valid types: {list(valid_types)}")

        mode = mode.lower()
        image_path = self._locate_image()

        if mode == 'pil.image':
            return Image.open(image_path)

        elif mode == 'np.array':
            image = np.array(Image.open(image_path))
            image[image[:, :, -1] == 0] = 255
            return image

        elif mode == 'pyglet.sprite':
            image = pyglet.image.load(image_path)
            sprite = pyglet.sprite.Sprite(img=image, x=self.x, y=self.y)
            return sprite


class RobotWorld:
    """
        Represent the robot world environment.

        :param Tuple[int, int] size:
            This is the grid size of the world. Where the first
            value is the number of grids on the x axis, and the second
            for the y axis.

        :param Union[None, Dict[Tuple[int, int], str]] mapping:
            Contains the information about non empty squares in the world.
            The keys represent the location of the sprite in x, y coordinates
            and the value is the sprite image name (without extension).
            If None is provided it will load a default map.
    """

    def __init__(self, size=constants.WORLD_SIZE, mapping=None):
        self.size: Size = Size(*size)
        self.mapping = mapping if mapping is not None else constants.MAP
        self.world = self._create_world(self.mapping)

        height = self.size.height * constants.SIZE_SQUARE
        width = self.size.width * constants.SIZE_SQUARE
        self._image = np.zeros((height, width, 4), dtype=np.uint8)
        self._grid = np.zeros(size, dtype=np.uint8)

    @classmethod
    def from_tuple(cls, size=constants.WORLD_SIZE, mapping=None):
        """ If the map was not given as a dictionary, but as [((x, y), name), ...]  """
        if mapping is None:
            return cls(size, mapping)
        mapping = {loc: name for loc, name in mapping}
        return cls(size, mapping)

    @property
    def immovable(self) -> List[Location]:
        """ Return all field locations that are occupied by non agent objects. """
        return [square.location for square in self.world if not square.sprite_name.startswith('agent')]

    @property
    def flag(self) -> List[Location]:
        """ return all flag position in the world.  """
        return [square.location for square in self.world if square.sprite_name == 'flag']

    @property
    def agents(self) -> List[Location]:
        """ Return all fields locations that contain an agent.  """
        return [square.location for square in self.world if square.sprite_name.startswith('agent')]

    @staticmethod
    def _create_world(mapping: Dict[Tuple[int, int], str]) -> List[Square]:
        """
            This creates a list of squares, that will represent the whole world.

            :param Dict[Tuple[int, int], str] mapping:
                Representation of the non empty squares, where the key is their
                x, y location and the value is the name of the sprite image.

            :return:
                A list of 'Squares', that can be used to represent the whole world.
        """
        return [Square(location, name) for location, name in mapping.items()]

    def image(self):
        """ Returns an RGBA image of the world.  """
        self._image.fill(255)  # Empty the image
        size = constants.SIZE_SQUARE

        for square in self.world:
            self._image[square.x: square.x + size, square.y: square.y + size] = square.image

        # Create grid on the image
        self._image[::size, :] = (0, 0, 0, 1)
        self._image[:, ::size] = (0, 0, 0, 1)
        return self._image

    def grid(self):
        """ 
            Returns a world size grid, representing the world. 
            The values are as follows:
            
            0: Passable terrain
            1: Immovable objects (blocked terrain)
            2: You the agent
            3: The final goal of the agent
        """
        self._grid.fill(0)
        for objects, value in [(self.immovable, 1), (self.agents, 2), (self.flag, 3)]:
            for loc in objects:
                self._grid[loc.x, loc.y] = value
        return self._grid

    def reset(self):
        """ Returns the world to the original start state.  """
        self.world = self._create_world(self.mapping)

    def render(self, image=None, delay=1):
        """ Renders the image of the world (note cv2 uses BGR instead of RGB).  """
        image = image if image is not None else self.image()
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        cv2.imshow(constants.CAPTION, image_bgr)
        cv2.waitKey(int(delay))
        return image

    def close(self):
        cv2.destroyWindow(constants.CAPTION)
