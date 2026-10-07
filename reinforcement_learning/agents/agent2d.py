from reinforcement_learning.agents.agent import Agent

import numpy as np

class Agent2D(Agent):
    def __init__(self, model, environment):
        super().__init__(model, environment)

    def act(self, state):
        # (-1, +1) (0,+1) (+1,+1)
        # (-1, 0)  (0, 0)  (+1, 0)
        # (-1,-1)  (0,-1)  (+1,-1)
        possible_actions = []

        for i in range(3):
            for j in range(3):
                # current position is not an action
                if i == 1 and j == 1:
                    continue

                if state[i, j] != 0:
                    di = i - 1
                    dj = j - 1

                    possible_actions.append((di, dj))

        if not possible_actions:
            return None
        
        return possible_actions[0]
        index = np.random.randint(len(possible_actions))
        return possible_actions[index]