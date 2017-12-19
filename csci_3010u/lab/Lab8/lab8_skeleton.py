import random
import simpy
import numpy as np
import matplotlib.pyplot as plt


RANDOM_SEED = 42
NUM_MACHINES = 3 # Number of machines in the carwash
WASHTIME = 10 # Minutes it takes to clean a car
T_INTER = 3 # Create a car every ~7 minutes
SIM_TIME = 200 # Simulation time in minutes

stats = {}
stats['cars'] = []
stats['waittimes'] = []
stats['totaltimes'] = []

class Carwash(object):
    """A carwash has a limited number of machines (``NUM_MACHINES``) to clean cars in parallel.
    Cars have to request one of the machines. 
    When they got one, they can start the washing processes and wait for it to finish (which takes ``washtime`` minutes).
    """
    def __init__(self, env, num_machines, washtime):
	self.env = env
	self.machine = simpy.Resource(env, num_machines)
	self.washtime = washtime
		
    def wash(self, car):
	"""The washing processes. It takes a ``car`` processes and tries to clean it."""
	yield self.env.timeout(random.randint(WASHTIME - 2, WASHTIME + 2))
	print("Carwash removed %d%% of %s's dirt." % (random.randint(50, 99), car))

def car(env, name, cw, stats):
    stats['cars'].append(name)
    print('%s arrives at the carwash at %.2f.' % (name, env.now))
    arrival_time = env.now
    with cw.machine.request() as request:
		
	yield request
	print('%s enters the carwash at %.2f.' % (name, env.now))
	enter_time = env.now
	yield env.process(cw.wash(name))
		
	print('%s leaves the carwash at %.2f.' % (name, env.now))
	leave_time = env.now
	
    stats['waittimes'].append(enter_time - arrival_time)
    stats['totaltimes'].append(leave_time - arrival_time)
	
def setup(env, num_machines, washtime, t_inter, stats): 
    """Create a carwash, a number of initial cars and keep creating cars approx. every ``t_inter`` minutes."""
    # Create the carwash
    carwash = Carwash(env, num_machines, washtime)
    # Create 4 initial cars
    for i in range(4):
	env.process(car(env, 'Car %d' % i, carwash, stats))

    # Create more cars while the simulation is running
    while True:
	yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
	i += 1
	env.process(car(env, 'Car %d' % i, carwash, stats))

# Setup and start the simulation
		
print('Carwash')
random.seed(RANDOM_SEED) 	

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER, stats))

# Execute!	
env.run(until=SIM_TIME)
	
print 'stats'
print stats

plt.figure()
plt.hist(stats['totaltimes'], color='crimson', edgecolor='black', linewidth=1.2)
plt.xlabel('Time (in minutes)')
plt.title('Total time spent in the carwash')
plt.ylabel('Number of cars')
plt.show()
