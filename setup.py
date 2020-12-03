#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup

setup(name="gym_robot",
      version="0.2",
      url="https://github.com/zoraiz-ali/gym.git",
      author="Zoraiz Ali",
      license="MIT",
      packages=["gym_robot", "gym_robot.envs"],
      
      install_requires = ["gym", "numpy"]
)

