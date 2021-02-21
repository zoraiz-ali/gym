from typing import Dict, Tuple

CAPTION = 'Deep Q-learning. Zoraiz Ali'

WORLD_SIZE = (11, 11)
SIZE_SQUARE = 40
FPS = 30

MAP: Dict[Tuple[int, int], str] = {
    (0, 0): 'agent_1', (0, 3): 'road_closed_1', (0, 4): 'road_closed_1', (0, 5): 'road_closed_1', (0, 6): 'road_closed_1',(0, 7): 'road_closed_1',
    (1, 3): 'road_closed_1', (1, 4): 'road_closed_1', (1, 5): 'road_closed_1', (1, 6): 'road_closed_1', (1, 7): 'road_closed_1',
    (2, 3): 'road_closed_1', (2, 4): 'road_closed_1', (2, 5): 'road_closed_1', (2, 6): 'road_closed_1', (2, 7): 'road_closed_1',
    (3, 3): 'road_closed_1', (3, 4): 'road_closed_1', (3, 5): 'road_closed_1', (3, 6): 'road_closed_1', (3, 7): 'road_closed_1',
    (4, 3): 'road_closed_1', (4, 4): 'road_closed_1', (4, 5): 'road_closed_1', (4, 6): 'road_closed_1', (4, 7): 'road_closed_1',
    (6, 3): 'road_closed_1', (6, 4): 'road_closed_1', (6, 5): 'road_closed_1', (6, 6): 'road_closed_1', (6, 7): 'road_closed_1',
    (7, 3): 'road_closed_1', (7, 4): 'road_closed_1', (7, 5): 'road_closed_1', (7, 6): 'road_closed_1', (7, 7): 'road_closed_1',
    (8, 3): 'road_closed_1', (8, 4): 'road_closed_1', (8, 5): 'road_closed_1', (8, 6): 'road_closed_1', (8, 7): 'road_closed_1',
    (9, 3): 'road_closed_1', (9, 4): 'road_closed_1', (9, 5): 'road_closed_1', (9, 6): 'road_closed_1', (9, 7): 'road_closed_1',
    (10, 3): 'road_closed_1', (10, 4): 'road_closed_1', (10, 5): 'road_closed_1', (10, 6): 'road_closed_1', (10, 7): 'road_closed_1',  (10, 10): 'flag',
}
