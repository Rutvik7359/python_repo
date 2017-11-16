from numpy import random
from math import exp
import numpy as np, matplotlib.pyplot as plt, sys


# =============================================================================
# Constants
# =============================================================================
LAT_DIMEN = 10
NUM_STEPS = 100
NUM_EQUIL = 1000
T         = np.linspace(1.2,3.8,256)


# =============================================================================
# Ising Model Functions
# =============================================================================
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


def set_boundary(i, j, N):
    _s = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    # boundary condition check and adjust
    if i == 0:
        _s[1][0] = N - 1
    elif i == (N-1):
        _s[0][0] = -(N-1)

    if j == 0:
        _s[3][1] = N - 1
    elif j == (N-1):
        _s[2][1] = -(N-1)

    return _s
    
def compute_energy(state):
    N = len(state)

    E = 0
    for i in range(N):
        for j in range(N):

            _s = set_boundary(i, j, N)
            s_neigh = 0
            for k in range(0, len(_s)):
                _i = i + _s[k][0]
                _j = j + _s[k][1]
                s_neigh += state[_i][_j]

            E += state[i][j]*s_neigh
    
    E *= -0.25

    return E

	
def compute_magnetization(state):
    N = len(state)

    M = 0
    for i in range(N):
        for j in range(N):
            M += state[i][j]

    return M

def mcstep(state, one_over_temp=1.):
    N = len(state)

    for _ in range (N*N):
        delta_E = 0
        i = random.randint(0, N)
        j = random.randint(0, N)

        _s = set_boundary(i, j, N)

        # get delta E for s(i,j)
        for k in range(0, len(_s)):
            _i = i + _s[k][0]
            _j = j + _s[k][1]
            delta_E += state[_i][_j]
        delta_E*= 2*state[i][j]

        if delta_E < 0:
            state[i][j] *= -1
        else:
            u = random.uniform(0, 1)
            if u < exp(-float(delta_E)*one_over_temp):
                state[i][j] *= -1

	return state
	

# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":

    N = LAT_DIMEN
    num_steps = NUM_STEPS

    arg_len = len(sys.argv) - 1
    error = False

    if arg_len > 2:
        error = True
    else:
        if arg_len >= 1:
            N = int(sys.argv[1])

            if arg_len == 2:
                num_steps = int(sys.argv[2])

    if error:
        print "Usage: python lab7.py <lattice_size>(optional) <num_steps>(optional)"
        sys.exit(0)

    E = [] # Energy
    M = [] # Magnetism
    C = [] # Specific Heat
    X = [] # Susceptibility

    for m in range(len(T)):
        Es = [] 
        E2s = []
        Ms = []
        M2s = []

        state = initialize(N, random='yes')

        if (m == 0):
            plt.figure(figsize=(4,4))
            ax = plt.subplot(111)
            plot_state(state, ax, 'Initial state')

        for i in range(NUM_EQUIL): # Run for some steps to achieve equilibrium
            state = mcstep(state, 1./T[m]) # before collecting statistics
        
        for i in range(num_steps): # Now sample states for num_steps and compute statistics
            state = mcstep(state, 1./T[m])

            Es.append(compute_energy(state))
            E2s.append(Es[-1]**2)
            Ms.append(compute_magnetization(state))
            M2s.append(Ms[-1]**2)

        E.append(float(sum(Es))/num_steps)
        M.append(float(sum(Ms))/num_steps)
        C.append((float(sum(E2s))/num_steps - E[-1]**2)/(T[m]**2))
        X.append((float(sum(M2s))/num_steps - M[-1]**2)/T[m])

    for i in range(len(M)):
        M[i] = abs(M[i])


    fig = plt.figure(figsize=(20, 10));
    plt.subplot(2, 2, 1 );
    plt.plot(T, E, 'o', color="red");
    plt.xlabel("Temperature (T)", fontsize=20);
    plt.ylabel("Energy ", fontsize=20);
    plt.subplot(2, 2, 2 );
    plt.plot(T, M, 'o', color="red");
    plt.xlabel("Temperature (T)", fontsize=20);
    plt.ylabel("Magnetization ", fontsize=20);
    plt.subplot(2, 2, 3 );
    plt.plot(T, C, 'o', color="red");
    plt.xlabel("Temperature (T)", fontsize=20);
    plt.ylabel("Specific Heat ", fontsize=20);
    plt.subplot(2, 2, 4 );
    plt.plot(T, X, 'o', color="red");
    plt.xlabel("Temperature (T)", fontsize=20);
    plt.ylabel("Susceptibility", fontsize=20);
    plt.show()