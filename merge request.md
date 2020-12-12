Based on your Stackoverflow
question ([here](https://stackoverflow.com/questions/65262795/motion-planning-of-robots-using-reinforcement-learning)).
I updated your code to be slightly more readable.

Change log:

- There is no longer a Tkinter program, but I use [opencv-python](https://pypi.org/project/opencv-python/) for the
  rendering of the image.
- There is now a 'RobotWorld' class that controls the world state and the rendering.
- The 'RobotEnv' class handles the interaction between the gym API and the 'RobotWorld'.
- The map creation has been made simpler, and an example can be viewed in the 'helper.constants' module.
- There is a skeleton code file in the folder 'agent', that contains the step that you have to do, in order to create a
  DQN agent.

Advice:

- Before trying to create a DQN agent on the image on this environment, you might want to first create a DQN agent on
  cartpole. Because the observation is much smaller and clearer. For this environment you might first want to create a
  small grid that represents every object as a number, which would lead to a much smaller robservation of (9x9x
  #objects). 
