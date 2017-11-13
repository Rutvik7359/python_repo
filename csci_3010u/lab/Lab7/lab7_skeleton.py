import numpy as np
import matplotlib.pyplot as plt

def initialize(N, random='yes'):
    '''Setting initial condition by assigning random spins'''
    if random == 'yes':
        state = 2*np.random.randint(2, size=(N,N))-1
    else:
        state = np.ones([N,N])
    return state

def plot_state(state, ax, title_str):
    w, h = state.shape
    X, Y = np.meshgrid(range(w), range(h))
    plt.xticks([])
    plt.yticks([])
    ax.pcolormesh(X, Y, state, cmap=plt.cm.bwr)
    plt.title(title_str)
    
def compute_magnetization(state):
	#TO DO
	return 

def compute_energy(state):
	#TO DO
	return state
	
def mcstep(state, one_over_temp=1.):
	#TO DO
	return 1
	
state = initialize(16, random='yes')
plt.figure(figsize=(4,4))
ax = plt.subplot(111)
plot_state(state, ax, 'Initial state')
plt.show()