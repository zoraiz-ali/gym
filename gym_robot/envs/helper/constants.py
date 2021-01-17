from typing import Dict, Tuple

CAPTION = 'Deep Q-learning. Zoraiz Ali'

WORLD_SIZE = (9, 9)
SIZE_SQUARE = 40
FPS = 30

MAP: Dict[Tuple[int, int], str] = {
    (0, 0): 'agent_1', (0, 1): 'road_closed_1', (0, 5): 'road_closed_1', (0, 8): 'road_closed_1',
    (1, 7): 'road_closed_1',
    (2, 0): 'road_closed_1', (2, 3): 'road_closed_1',
    (3, 2): 'road_closed_1', (3, 5): 'road_closed_1', (3, 7): 'road_closed_1', (3, 8): 'road_closed_1',
    (4, 0): 'road_closed_1', (4, 3): 'road_closed_1',
    (5, 5): 'road_closed_1', (5, 6): 'road_closed_1', (5, 7): 'road_closed_1',
    (6, 1): 'road_closed_1', (6, 5): 'road_closed_1', (6, 6): 'flag', (6, 7): 'road_closed_1',
    (7, 3): 'road_closed_1', (7, 5): 'road_closed_1', (7, 7): 'road_closed_1',
    (8, 0): 'road_closed_1',
}
