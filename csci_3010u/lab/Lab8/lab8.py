import random, simpy, time, numpy as np, matplotlib.pyplot as plt
from scipy.stats import norm


RANDOM_SEED = 42
NUM_WASH_STATIONS = 2 # Number of machines in the carwash
NUM_DRY_STATIONS = 1 # Number of machines in the carwash
ARRIVALTIME = [3, 4, 5, 3, 3, 4, 9, 10]
WASHTIME = [5, 5, 5, 6, 6, 5, 5, 5, 5] # Minutes it takes to clean a car
DRYTIME = [1.5, 1.5, 1.7, 1.5, 1.5, 1.5, 1.7, 1.5, 1.4] # Minutes it takes to clean a car
T_INTER = 3 # Create a car every ~7 minutes
SIM_TIME = 200 # Simulation time in minutes

stats = {}
stats['cars'] = []
stats['waittimes'] = []
stats['totaltimes'] = []

class Carwash(object):
    """
    A carwash has a limited number of machines (``NUM_MACHINES``) to clean cars
    in parallel. Cars have to request one of the machines. When they got one,
    they can start the washing processes and wait for it to finish (which takes
    ``washtime`` minutes).
    """
    def __init__(self, env, num_wash_stations, num_dry_stations, wash_time, dry_time):
    	self.env = env
        self.wash_station = simpy.Resource(env, num_wash_stations)
    	self.dry_station = simpy.Resource(env, num_dry_stations)
    	self.wash_time = wash_time
        self.dry_time = dry_time

		
    def wash(self, car):
    	"""The washing processes. It takes a ``car`` processes and tries to wash it."""
    	yield self.env.timeout(random.choice(self.wash_time))

    def dry(self, car):
        """The drying processes. It takes a ``car`` processes and tries to dry it."""
        yield self.env.timeout(random.choice(self.dry_time))

def car(env, name, cw, stats):
    """
    The car process (each car has a ``name``) arrives at the carwash(``cw``) 
    and requests a cleaning machine. It then starts the washing process, waits
    for it to finish and leaves to never come back ...
    """
    arrival_time = env.now
    name = name + " " + str(arrival_time)
    stats['cars'].append(name)
    
    with cw.wash_station.request() as request:
    	yield request
    	print('%s enters the car wash machine at %.2f.' % (name, env.now))
    	enter_time = env.now
    	yield env.process(cw.wash(name))
    		
    	print('%s leaves the car wash machine at %.2f.' % (name, env.now))

        stats['waittimes'].append(round(enter_time - arrival_time, 2))


    dry_arrival_time = env.now
    with cw.dry_station.request() as request:
        yield request
        print('%s enters the car dry machine at %.2f.' % (name, env.now))
        enter_time = env.now
        yield env.process(cw.dry(name))
            
        print('%s leaves the car dry machine at %.2f.' % (name, env.now))
        leave_time = env.now

        stats['waittimes'][-1] += (round(enter_time - dry_arrival_time, 2))
        stats['totaltimes'].append(round(leave_time - arrival_time, 2))

	
def setup(env, num_wash_stations, num_dry_stations, wash_time, dry_time, arrival_time, stats): 
    """
    Create a carwash, a number of initial cars and keep creating cars approx.
    every ``t_inter`` minutes.
    """
    # Create the carwash
    carwash = Carwash(env, num_wash_stations, num_dry_stations, wash_time, dry_time)
    # Create 4 initial cars
    for i in range(4):
	   env.process(car(env, 'Car', carwash, stats))

    # Create more cars while the simulation is running
    while True:
	   yield env.timeout(random.choice(arrival_time))
	   i += 1
	   env.process(car(env, 'Car', carwash, stats))



# Setup and start the simulation
print('Carwash')
random.seed(RANDOM_SEED) 	

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_WASH_STATIONS, NUM_DRY_STATIONS, WASHTIME, DRYTIME, ARRIVALTIME, stats))

# Execute!	
env.run(until=SIM_TIME)
	
print 'stats'
print stats
print sum(stats['totaltimes'])/len(stats['totaltimes'])
print sum(stats['waittimes'])/len(stats['waittimes'])

plt.figure(1)
plt.hist(stats['totaltimes'], color='crimson', edgecolor='black', linewidth=1.2)
plt.xlabel('Time (in minutes)')
plt.title('Total time spent in the carwash')
plt.ylabel('Number of cars')
plt.figure(2)
plt.hist(stats['waittimes'], color='crimson', edgecolor='black', linewidth=1.2)
plt.xlabel('Time (in minutes)')
plt.title('Total wait time in the carwash')
plt.ylabel('Number of cars')
plt.show()