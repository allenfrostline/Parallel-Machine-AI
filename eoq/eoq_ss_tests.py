import numpy as np
import matplotlib.pylab as plt
from matplotlib2tikz import save as tikz_save

from matplotlib import style
style.use('ggplot')


D = 4  # demand per period
h = 1  # holding cost per unit per time
p = 20 # selling price per item
K = 10  # order cost
I_max = 20
Q_max = 10  # maximum order size

state_space = list(range(I_max+1))
action_space = list(range(Q_max))


def max_total(scenario):
    # maximize the total reward during a finite horizon
    num_episodes = scenario['num_episodes']
    length_episode = scenario['length_episode']
    beta = scenario['beta']

    np.random.seed(3)
    Q = np.zeros([len(state_space), len(action_space)])
    hits = np.zeros([len(state_space), len(action_space)])

    for i in range(num_episodes):
        I = 0
        alpha = 0.99
        thres = beta(i)
        for _ in range(length_episode):
            if np.random.rand(1) < thres:
                u = np.argmax(Q[I, :])
            else:
                u = np.random.choice(action_space)
            D = np.random.randint(3,5)
            # D = 4
            S = min(I + u, D)  # sales
            I1 = min(I + u - S, I_max)
            R = p*S - h*I1 - K*(u>0)

            #  Update Q-Table with new knowledge
            Q[I, u] = R + alpha*np.max(Q[I1, :])
            hits[I,u] += 1
            I = I1
    return Q, hits

scenario_2 = {
    'name': "scenario_2",
    'length_episode': 10000,
    'num_episodes': 1,
    'beta': lambda x: 0.8
    #'beta': lambda x: 0.8 + 0.2*x/2000
    }

Q, hits = max_total(scenario_2)
np.set_printoptions(precision=1)
print("Final Q-Table Values")
print(Q)
print(np.argmax(Q, axis=1))

print(hits)


