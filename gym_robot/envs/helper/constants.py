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
