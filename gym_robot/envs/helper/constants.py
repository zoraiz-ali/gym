from typing import Dict, Tuple

CAPTION = 'Deep Q-learning. Zoraiz Ali'

WORLD_SIZE = (9, 9)
SIZE_SQUARE = 40
FPS = 30

MAP: Dict[Tuple[int, int], str] = {
    (0, 0): 'black', (0 , 1): 'agent_1', (0, 3): 'black', (0, 4): 'black', (0, 5): 'black', (0, 6): 'black',(0, 7): 'black',
    (1, 3): 'black', (1, 4): 'black', (1, 5): 'black', (1, 6): 'black', (1, 7): 'black',
    (2, 3): 'black', (2, 4): 'black', (2, 5): 'black', (2, 6): 'black', (2, 7): 'black',
    (3, 3): 'black', (3, 4): 'black', (3, 5): 'black', (3, 6): 'black', (3, 7): 'black',
    (4, 3): 'black', (4, 4): 'black', (4, 5): 'black', (4, 6): 'black', (4, 7): 'black',
    (6, 3): 'black', (6, 4): 'black', (6, 5): 'black', (6, 6): 'black', (6, 7): 'black',
    (7, 3): 'black', (7, 4): 'black', (7, 5): 'black', (7, 6): 'black', (7, 7): 'black',
    (8, 3): 'black', (8, 4): 'black', (8, 5): 'black', (8, 6): 'black', (9, 9): 'flag',
    
}
