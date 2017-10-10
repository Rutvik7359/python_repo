import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.integrate import ode
import time

# Color
# =============================================================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

HEIGHT_TOP = 800
HEIGHT_BOT = 600

DATA_FILE = 'data.csv'

# Setup environment vars
# =============================================================================
N_MASS        = 5 #masses
MASS          = 5 #kg
GRAVITY_CONST = -9.8 #m/s^2
TIME_STEP     = 0.1

SPRING_EQUIL = 200 #m
SPRING_CONST = 0.4

INIT_PAUSED = False
INIT_DROP   = True
USE_DAMPER  = True
DAMP_CONST  = 0.2

Y_VY_TOL = 1 # setting lower limit of y and vy

# clock object that ensure that animation has the same
# on all machines, regardless of the actual machine speed.
clock = pygame.time.Clock()

def load_image(name):
    image = pygame.image.load(name)
    return image

class MyCircle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.circle(self.image, color, (int(width/2), int(height/2)), cx, cy)
        self.rect = self.image.get_rect()

    def update(self):
        pass

class Simulation:
    def __init__(self):
        self.y    = np.array([0, 0])
        self.vy   = np.array([0, 0])
        self.mass = 0
        self.dt   = 0
        self.n    = 0

        self.grav = 0
        self.k    = 0
        self.equi = 0
        self.damp = 0

        self.paused      = True
        self.init_drop   = True
        self.n_mass_used = True

        self.times = []
        self.positions = []
        self.velocities = []

        self.rest_position = 0

        self.cur_time = 0
        self.solver   = ode(self.f)
        self.solver.set_integrator('dop853')

    # Setup to start from top of the screen or from last recorded position
    # with last recorded velocity
    def setup(self, y, vy, mass):
        self.y    = y
        self.vy   = vy
        self.dt   = TIME_STEP 
        self.n    = len(y)    # number of masses
        self.mass = mass/self.n # slinky mass divided by n masses

        self.grav = GRAVITY_CONST            # gravity 
        self.k    = SPRING_CONST*(self.n-1)  # spring constant
        self.equi = SPRING_EQUIL/(self.n-1)  # spring equilibrium
        if USE_DAMPER:
            self.damp = DAMP_CONST               

        self.n_mass_used = (self.n > 2)

        self.paused    = INIT_PAUSED
        self.init_drop = INIT_DROP

        self.times = []
        self.positions =  [[] for i in range(self.n)]
        self.velocities = [[] for i in range(self.n)]

        self.cur_time = 0

        self.solver.set_initial_value(self.appendList([self.y, self.vy]), self.cur_time)

    def f(self, t, state):

        # setup y change in spring length between each mass
        y = []
        for i in range(0, self.n-1):
            y.append(self.equi -(state[i]-state[i+1]))

        nth_force = np.abs(self.grav*self.mass - self.k*y[-1])
        dy = np.zeros(self.n)
        dvy = np.zeros(self.n)

        # While the top of the slinky is held
        if self.init_drop:
            dy[0], dvy[0] = 0, 0
            dy[-1], dvy[-1] = state[-1], self.getDvy(y[-1], state[-1], -1)

            # Stop movement after the initial drop when force and velocity under 0.7
            if (nth_force + np.abs(state[-1])) < Y_VY_TOL*2:
                dy = np.zeros(self.n)
                dvy = np.zeros(self.n)
                self.rest_position = state[self.n-1]
                self.init_drop = False

        # dy and dvy calculations once the top of the slinky is let go
        else:
            dy[0],  dvy[0]  = state[self.n], self.getDvy(y[0], state[self.n])
            dy[-1], dvy[-1] = state[-1],     self.getDvy(y[-1], state[-1], -1)

        if self.n_mass_used:
            dy[1:self.n-1]  = state[self.n+1:self.n*2-1]
            dvy[1:self.n-1] = self.getMidDvy(y, state[self.n:])

        return self.appendList([dy, dvy])

    def step(self):
        self.cur_time += self.dt

        if self.solver.successful():
            self.solver.integrate(self.cur_time)
            self.y = self.solver.y[0:self.n]
            self.vy = self.solver.y[self.n:self.n*2]

            # add positions and velocities to graph from when top of slinky is
            # released and top of slinky has passed the initial position of the
            # bottom of slinky when the top was released (Observing C-E)
            if not self.y[0] < self.rest_position:
                if not self.init_drop:
                    self.times.append(self.cur_time)
                    for i in range(0, self.n):
                        self.positions[i].append(self.y[i])
                        self.velocities[i].append(self.vy[i])

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False


    # Helper functions
    # =========================================================================
    # Calculate dvy for all the masses inclusivley between m[0] and m[n-1]
    # where n = len(dy)
    # =========================================================================
    def getMidDvy(self, y, dy):
        n_dy = len(dy)

        dvy = []
        for i in range(1, n_dy-1):
            dvy.append(self.getDvy(y[i] - y[i-1] , dy[i]))
        return dvy    

    # =========================================================================
    # Calculate dvy based on y
    # =========================================================================
    def getDvy(self, y, dy, dir=1):
        return (dir*self.k*y - self.damp*dy)/self.mass + self.grav

    # =========================================================================
    # Append list items one by one to a list
    # =========================================================================
    def appendList(self, lists):
        list = []

        n_lists = len(lists)
        for i in range(0, n_lists):
            items  = lists[i]
            n_item = len(items)
            for j in range(0, n_item):
                list.append(items[j])

        return list

# Prints usage
def usage():
    one_line = '-'*55
    two_line = one_line + '\n' + one_line
    print '\n' + one_line
    print 'Usage:'
    print one_line
    print 'python a1.py <n_#_of_masses>'
    print 'or'
    print 'python a1.py'
    print two_line
    print 'During Simulation:'
    print one_line
    print 'Press (r) to start/resume simulation'
    print 'Press (p) to pause simulation'
    print 'Press (q) to quit simulation'
    print 'Press (space) to step forward simulation when paused'
    print two_line + '\n'

def sim_to_screen_y(win_height, y):
    '''flipping y, since we want our y to increase as we move up'''
    return win_height - y

def main():

    # get N masses from command line arg
    # usage pythong a1.py <n_#_of_masses>
    num_args = len(sys.argv) - 1
    if num_args == 2:
        n_mass = int(sys.argv[1])
        # min mass of n_mass kg
        mass = min(n_mass, int(sys.argv[2]))
    elif num_args == 1:
        n_mass = int(sys.argv[1])
        mass = n_mass
    elif num_args > 2:
        usage()
        sys.exit(0)
    else:
        n_mass = N_MASS
        mass = MASS


    # initializing pygame
    pygame.init()

    end_of_screen = False;

    # top left corner is (0,0) top right (640,0) bottom left (0,480)
    # and bottom right is (640,480).
    win_width = 640
    win_height = HEIGHT_TOP
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('1D Ball in Free Fall')

    # setting up N sprite groups and sprites
    my_sprite = []
    my_group = []
    for i in range(0, n_mass):
        my_sprite.append(MyCircle(RED, 30, 30))
        my_group.append(pygame.sprite.Group(my_sprite[i]))
    
    # setup N positions an velocities(1 for each mass)
    y  = []
    vy = []
    yspring = HEIGHT_TOP - HEIGHT_BOT
    yinit   = HEIGHT_TOP
    ystep   = yspring/(n_mass-1)
    for i in range(0, n_mass):
        y.append(yinit)
        vy.append(0)
        yinit -= ystep


    # setting up simulation
    sim = Simulation()
    sim.setup(y, vy, mass)

    usage()

    while True:
        # 30 fps
        clock.tick(30)

        # update sprite x, y position using values
        # returned from the simulation
        for i in range(0, n_mass):
            my_sprite[i].rect.x = win_width/2
            my_sprite[i].rect.y = sim_to_screen_y(win_height, sim.y[i])

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            sim.pause()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            sim.resume()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            break
        else:
            pass

        # clear the background, and draw the sprites
        screen.fill(WHITE)

        for i in range(0, n_mass):
            my_group[i].update()
            my_group[i].draw(screen)
        pygame.display.flip()

        if sim_to_screen_y(win_height, sim.y[0]) > win_height:
            end_of_screen = True
            pygame.quit()
            break

        # update simulation
        if not sim.paused:
            sim.step()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sim.step()

    # Using matplotlib to plot simulation data
    plt.figure(figsize=(7,9))

    plt.subplot(211)
    for i in range(0, len(sim.positions)):
        plt.plot(sim.times, sim.positions[i], linewidth=0.6)
    plt.ylabel('Height (m)')
    plt.title('Height vs. Time')

    # velocity vs time data to plot
    plt.subplot(212)
    for i in range(0, len(sim.velocities)):
        plt.plot(sim.times, sim.velocities[i], linewidth=0.6)
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity vs. Time')


    plt.tight_layout(2)
    plt.show()
if __name__ == '__main__':
    main()
