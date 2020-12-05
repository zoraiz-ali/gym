#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_robot.envs.gym_robot2d import Environment


class RobotEnv(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
    }
    
    def __init__(self, agent):
        self.environment = Environment()
        self.action_space = spaces.Discrete(4)
        low = np.zeros(self.environment.reset(), dtype=int)
        high = np.ones(self.environment.reset(), dtype=int)
        self.observation_space = spaces.Box(low, high, dtype=np.int)
        
        
    def reset(self):
        del self.environment
        self.environmet = Environment()
        obs = self.environment.reset()
        return obs  
    
    
    def step(self, action):
        self.environment.action(action)       
        return  next_state, reward, done
    
    def render(self, mode="human", close=False):
        self.environment.render()
    

