import cv2
import numpy as np

from typing import Tuple, Dict, List

from gym_robot.envs import constants
from gym_robot.envs.helper import Size, Location, Square


class World:
    """
        Represent the robot world environment.

        :param Tuple[int, int] size:
            This is the grid size of the world. Where the first
            value is the number of grids on the x axis, and the second
            for the y axis.

        :param Union[None, Dict[Tuple[int, int], str]} mapping:
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
        return [square.location for square in self.world]

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


if __name__ == '__main__':
    world = World()
    world.render(delay=0)
