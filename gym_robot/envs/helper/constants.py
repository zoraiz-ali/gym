from typing import Dict, Tuple

CAPTION = 'Deep Q-learning. Zoraiz Ali'

WORLD_SIZE = (9, 9)
SIZE_SQUARE = 40
FPS = 30

MAP: Dict[Tuple[int, int], str] = {
    (0, 0): 'agent_1', (0, 1): 'black', (0, 5): 'black', (0, 8): 'black',
    (1, 7): 'black',
    (2, 0): 'black', (2, 3): 'black',
    (3, 2): 'black', (3, 5): 'black', (3, 7): 'black', (3, 8): 'black',
    (4, 0): 'black', (4, 3): 'black',
    (5, 5): 'black', (5, 6): 'black', (5, 7): 'black',
    (6, 1): 'black', (6, 5): 'black', (6, 6): 'flag', (6, 7): 'black',
    (7, 3): 'black', (7, 5): 'black', (7, 7): 'black',
    (8, 0): 'black',
}
