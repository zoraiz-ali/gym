"""
This file contains skeleton code for a DQN agent, based of the

    - https://pylessons.com/CartPole-reinforcement-learning/

The main steps are outlined, it is up to you to fill in the missing code.
Make sure to have a good look at the above link for the missing code.

"""


class DQNAgent:

    def __init__(self):
        # Generate the environment, and define the input and output shape of your model.
        # At the beginning completely disregard epsilon, build that in later.

        # Create your model:
        pass

    def create_model(self, input_shape, output_shape):
        # Build a keras / pytorch / tensorflow model.
        # Please note that we will probably have to use `Conv2D` layers, because we have an image.
        # Dense layers are good for finding connections between all input data, while Convolutional layers
        # are better at finding local relations.
        # (a pixel on the left top should have no real impact on a pixel on the right bottom.)
        pass

    def run(self, nr_games, render):
        # This will run your DQN model on a specified environment (self.env)
        # Start by creating a normal gym loop without using the keras model, using random actions.
        # When that is working as expected and you retrieve the right observation (check shape),
        # let the model make predictions based on the observation (don't use them yet).
        # Then, start implementing the replay memory (the method 'remember'),
        # make again sure that everything is still working correctly as expected.
        # After creating the replay memory, generate the model 'replay' method (this is where your model learns)
        pass

    def remember(self, state, action, reward, next_state, done):
        # This is where you add all your experiences (transitions) to the agents memory.
        # When using this, take into account that for images a large part of memory has to be
        # reserved. Start small, with at most 1_000 images, and you will already use 3 GB of  Memory
        # (Width = 9*40, height = 9 *40, depth = 3, np.uint8 = 8 bytes -> 360*360*3*8 ~ 3Mb, 1_000 images ~ 3GB)
        pass

    def replay(self):
        # This is where you implement the update formula of the DQN
        # Q(s, a) = R + \gamma * max(Q(s'))
        #
        # Make sure to take your time and understand this step, because it comes back a lot.
        # The real thing to remember here is that you are predicting the reward that you will get
        # for a certain state action pair.
        # E.g: When I am in this state, and I go left I expect to get a final score of 1.
        pass
