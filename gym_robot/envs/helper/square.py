import os
import numpy as np

import pyglet

from typing import Tuple
from pathlib import Path
from dataclasses import dataclass
from PIL import Image

from gym_robot.envs.helper import constants


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
