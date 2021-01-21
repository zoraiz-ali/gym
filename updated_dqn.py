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
        self.memory = deque(maxlen = 200000)

        self.gamma = 0.95
        self.epsilon = 0.9
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate= 0.5
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
        #if self.epsilon > self.epsilon_min:
            #self.epsilon *= self.epsilon_decay
    
    def load (self, name):
        self.model.load_weights(name)

    def save (self, name):
        self.model.save_weights(name)    
        
    # Plotting the results for the number of steps
    def plot_results(self, steps):
                  
                    #
                    plt.figure()
                    plt.plot(np.arange(len(steps_per_episode)),steps_per_episode, 'b')
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
    steps_per_episode = []
    for episode in range(1001):
        state = env.reset()
        state = np.reshape(state, [1, 9,9])
        done = False
        score = 0
        i = 0
        cost = 0
        while not done :
            env.render()
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            i += 1
            if not done: 
                reward = reward
            score += reward
            
                
            next_state = np.reshape(next_state, [1, 9,9])
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            if done:
                steps_per_episode.append(i)
                print("episode: {},step:{}, step: {}, e: {:.2}"
                      .format(episode, i, steps_per_episode,agent.epsilon))
                
                
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
agent.plot_results( steps_per_episode)          
       
