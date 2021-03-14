import random
import gym
import gym_robot   
import gym_robot.envs
import gym_robot.envs.helper
import numpy as np
import pyglet
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
import matplotlib.pyplot as plt



class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
   
   #we make memory to train our agent
        self.memory = deque(maxlen = 20000)

        self.gamma = 0.95
        self.epsilon = 0.9
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate= 0.001
        self.model = self._build_model()
        #self.model = OurModel(input_shape=(self.state_size), action_space = self.action_size)
    
    


    def _build_model(self):
        model = Sequential()
        model.add(Flatten(input_shape=self.state_size))
        model.add(Dense(128, activation='linear'))
        model.add(Dense(128, activation='linear'))        
        model.add(Dense(self.action_size, activation='linear'))

        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model
      
    def memorize(self, state, action, reward, next_state, done):
        self.memory.append(( state, action, reward, next_state, done))     
    

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)            
        act_values = self.model.predict(state)        
        return np.argmax(act_values)
        
        
    

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
        
   
    def plot_results(self, steps, score):
                  
                    #
                    plt.figure()
                    plt.plot(np.arange(len(steps_per_episode)),steps_per_episode )
                    plt.title('Episode via steps')
                    plt.xlabel('EPISODES')
                    plt.ylabel('steps')
                    
                    plt.figure()
                    plt.plot(np.arange(len(score_per_episode)),score_per_episode )
                    plt.title('Episode via score')
                    plt.xlabel('EPISODES')
                    plt.ylabel('score')

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
    score_per_episode = []
    for episode in range(1000):
        state = env.reset()
        state = np.reshape(state, [1, 9,9])
        done = False
        score = 0
        i = 0
        
        while not done :
            env.render()
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            i += 1
            score +=reward
            if not done: 
                reward = reward
            
            
                
            next_state = np.reshape(next_state, [1, 9,9])
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            if done:
                steps_per_episode.append(i)
                score_per_episode.append(score)
                print("episode: {},step:{}, step: {}, score: {},  e: {:.2}"
                      .format(episode, i, steps_per_episode, score,   agent.epsilon))
                
                
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
agent.plot_results( steps_per_episode, score_per_episode)          
       
