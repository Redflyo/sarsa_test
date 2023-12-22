import random
import numpy as np

class SARSA:
    def __init__(self, action_space, alpha=0.1, gamma=0.9, epsilon=0.9):
        self.action_space = action_space
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = {}

    def set_Q_value(self,state,index_action,value):
        if state in self.Q:
            (self.Q[state])[index_action] = value
        else:
            self.Q[state] = np.zeros(len(self.action_space))
            self.Q[state][index_action] = value

   
    def get_Q_values_by_state(self,state):
        if state in self.Q:
            return self.Q[state]
        else:
            self.Q[state] = np.zeros(len(self.action_space))
            return self.Q[state]
        
    def get_Q_value(self,state,action):            
        return self.get_Q_values_by_state(state)[action]
    
    def choose_action(self, state,epsilon):
        if random.uniform(0, 1) < epsilon:
            action_index = random.choice(range(len(self.action_space)))
        else:
            action_index = np.argmax(self.get_Q_values_by_state(state))
        return action_index

    def update(self, state, action, reward, next_state, next_action):
        predict = self.get_Q_value(state, action)
        target = reward + self.gamma * self.get_Q_value(next_state,next_action)
        new_Q_value = predict + self.alpha * (target - predict)
        self.set_Q_value(state,action,new_Q_value)

    def train(self, episodes,game):
        for episode in range(episodes):
            epsilon = -self.epsilon/episodes * episode + self.epsilon
            env = game()
            state = env.get_state()
            action = self.choose_action(state,epsilon)
            total_reward = 0
            done = False
            while not done:
                reward, done, = env.step(self.action_space[action])
                next_state = env.get_state()
                next_action = self.choose_action(next_state,epsilon)
                self.update(state, action, reward, next_state, next_action)
                state = next_state
                action = next_action
                total_reward += reward
            print(f"Episode {episode + 1}, Total Reward: {total_reward}")