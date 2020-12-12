#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from gym.envs.registration import register

register(
        id='robot-v0',
        entry_point='gym_robot.envs:RobotEnv',
        max_episode_steps=2000,
)

register(
        id='robot-v1',
        entry_point='gym_robot.envs:RobotEnv',
        max_episode_steps=2000,
        kwargs=dict(obs_mode='grid')
)
