from typing import Dict, Tuple

CAPTION = 'Deep Q-learning. Zoraiz Ali'

WORLD_SIZE = (9, 9)
SIZE_SQUARE = 40
FPS = 30

MAP: Dict[Tuple[int, int], str] = {
    (0, 0): 'agent_1', 
    (1, 3): 'black', (1, 4): 'black', (1, 5): 'black', (1, 6): 'black', 
    (2, 3): 'black', (2, 4): 'black', (2, 5): 'black', (2, 6): 'black', (2, 7): 'black',
    (3, 7): 'black',
    (4, 4): 'black',
    (5,0): 'black', (5,2): 'black', (5,4): 'black',
    (7, 3): 'black', (7, 4): 'black', (7, 5): 'black', (7, 6): 'black', (7, 7): 'black',
    (8,8): 'flag',
    
}
