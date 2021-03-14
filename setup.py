#!/usr/bin/env python
# coding: utf-8


from setuptools import setup

setup(
        name="gym_robot",
        version="0.3",
        url="https://github.com/zoraiz-ali/gym.git",
        author="Zoraiz Ali",
        license="MIT",
        packages=["gym_robot", "gym_robot.envs", "gym_robot.envs.helper", ],
        include_package_data=True,
        install_requires=["gym", "numpy", "opencv-python", "pillow"]
)
