import random
import gym
import gym_robot   
import gym_robot.envs
import gym_robot.envs.helper
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
import matplotlib.pyplot as plt

EPISODES = 10






class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
   
   #we make memory to train our agent
        self.memory = deque(maxlen = 2000)

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate= 0.01
        self.model = self._build_model()
        #self.model = OurModel(input_shape=(self.state_size), action_space = self.action_size)
    
    
### build our model

    def _build_model(self):
        model = Sequential()
        model.add(Flatten(input_shape=self.state_size))
        model.add(Dense(512, activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model
      
    def memorize(self, state, action, reward, next_state, done):
        self.memory.append(( state, action, reward, next_state, done))     
    
# what action to take at given state
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)            
        act_values = self.model.predict(state)        
        return np.argmax(act_values)
        
        
    
# define method to train our agent
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def load (self, name):
        self.model.load_weights(name)

    def save (self, name):
        self.model.save_weights(name)    
        
    # Plotting the results for the number of steps
    def plot_results(self, steps):
                  
                    #
                    plt.figure()
                    plt.plot(np.arange(steps), steps, 'b')
                    plt.title('Episode via steps')
                    plt.xlabel('EPISODES')
                    plt.ylabel('steps')      

                   # Showing the plots
                    plt.show()
       
if __name__ == "__main__":
    env = gym.make('robot-v1')
    state_size = env.observation_space.shape
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    #agent.model.summary()
    done = False
    batch_size = 32

    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, 9,9])
        done = False
        score = 0
        steps = 0
        cost = 0
        while not done:
            env.render()
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
           
            if not done: 
                reward = reward
            score += reward
            steps += 1
            
            next_state = np.reshape(next_state, [1, 9,9])
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            if done:
                print("episode: {}/{}, step: {}, e: {:.2}"
                      .format(e, EPISODES, steps, agent.epsilon))
                
                
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    agent.plot_results( steps)
    
    
    #Output
 episode: 0/10, step: 22, e: 1.0
episode: 1/10, step: 1, e: 1.0
episode: 2/10, step: 5, e: 1.0
episode: 3/10, step: 12, e: 0.97
episode: 4/10, step: 4, e: 0.95
episode: 5/10, step: 13, e: 0.9
episode: 6/10, step: 3, e: 0.89
episode: 7/10, step: 2, e: 0.88
episode: 8/10, step: 7, e: 0.86
episode: 9/10, step: 3, e: 0.85
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-1-3c74082a72ba> in <module>
    131             if len(agent.memory) > batch_size:
    132                 agent.replay(batch_size)
--> 133     agent.plot_results( steps)
    134 

<ipython-input-1-3c74082a72ba> in plot_results(self, steps)
     86                     #
     87                     plt.figure()
---> 88                     plt.plot(np.arange(steps), steps, 'b')
     89                     plt.title('Episode via steps')
     90                     plt.xlabel('EPISODES')

~\anaconda3\lib\site-packages\matplotlib\pyplot.py in plot(scalex, scaley, data, *args, **kwargs)
   2759 @docstring.copy(Axes.plot)
   2760 def plot(*args, scalex=True, scaley=True, data=None, **kwargs):
-> 2761     return gca().plot(
   2762         *args, scalex=scalex, scaley=scaley, **({"data": data} if data
   2763         is not None else {}), **kwargs)

~\anaconda3\lib\site-packages\matplotlib\axes\_axes.py in plot(self, scalex, scaley, data, *args, **kwargs)
   1645         """
   1646         kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D)
-> 1647         lines = [*self._get_lines(*args, data=data, **kwargs)]
   1648         for line in lines:
   1649             self.add_line(line)

~\anaconda3\lib\site-packages\matplotlib\axes\_base.py in __call__(self, *args, **kwargs)
    214                 this += args[0],
    215                 args = args[1:]
--> 216             yield from self._plot_args(this, kwargs)
    217 
    218     def get_next_color(self):

~\anaconda3\lib\site-packages\matplotlib\axes\_base.py in _plot_args(self, tup, kwargs)
    340 
    341         if x.shape[0] != y.shape[0]:
--> 342             raise ValueError(f"x and y must have same first dimension, but "
    343                              f"have shapes {x.shape} and {y.shape}")
    344         if x.ndim > 2 or y.ndim > 2:

ValueError: x and y must have same first dimension, but have shapes (3,) and (1,)

