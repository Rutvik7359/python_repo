import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DATA_FILE = 'data.csv'

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
        self.y = 0
        self.vy = 0
        self.mass = 0
        self.g = -9.8 # gravity acts downwards
        self.dt = 0.033 # 33 millisecond, which corresponds to 30 fps
        self.cur_time = 0

        self.paused = True # starting in paused mode

    # Setup to start from top of the screen or from last recorded position
    # with last recorded velocity
    def setup(self, y, vy, mass):
        self.y = y
        self.vy = vy
        self.mass = mass

        self.times = [self.cur_time*1000]
        self.positions = [self.y]
        self.velocities = [self.vy]

    def step(self):
        self.y += self.vy
        self.vy += self.mass * self.g * self.dt
        self.cur_time += self.dt

        self.times.append(self.cur_time * 1000)
        self.positions.append(self.y)
        self.velocities.append(self.vy)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

def sim_to_screen_y(win_height, y):
    '''flipping y, since we want our y to increase as we move up'''
    return win_height - y

# Helper function to write data to csv file
# Data input is array of position values and velocity values
def write_to_file(file, data):
    with open(file, 'w') as data_csv:
        writer=csv.writer(data_csv, delimiter=',')
        writer.writerows(zip(data[0], data[1]))

# Helper function to read from csv file and return two values
# Return (last_recorded_position, last_recorded_velocity) 
def last_vals_from_file(file):
    with open(file, 'r') as data_csv:
        reader = list(csv.reader(data_csv))
        return reader[-1][0], reader[-1][1]


def main():

    # initializing pygame
    pygame.init()

    end_of_screen = False;

    # top left corner is (0,0) top right (640,0) bottom left (0,480)
    # and bottom right is (640,480).
    win_width = 640
    win_height = 480
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('1D Ball in Free Fall')

    # setting up a sprite group, which will be drawn on the
    # screen
    my_sprite = MyCircle(RED, 30, 30)
    my_group = pygame.sprite.Group(my_sprite)

    
    (y, vy) = (460,0)
    if os.path.exists(DATA_FILE):
        data = last_vals_from_file(DATA_FILE)
        (y, vy) = (float(data[0]), float(data[1]))

    # setting up simulation
    sim = Simulation()
    sim.setup(y, vy, 1)

    print ('--------------------------------')
    print ('Usage:')
    print ('Press (r) to start/resume simulation')
    print ('Press (p) to pause simulation')
    print ('Press (q) to quit simulation')
    print ('Press (space) to step forward simulation when paused')
    print ('--------------------------------')

    while True:
        # 30 fps
        clock.tick(30)

        # update sprite x, y position using values
        # returned from the simulation
        my_sprite.rect.x = win_width/2
        my_sprite.rect.y = sim_to_screen_y(win_height, sim.y)

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
        my_group.update()
        my_group.draw(screen)
        pygame.display.flip()

        if sim_to_screen_y(win_height, sim.y) > win_height:
            end_of_screen = True
            pygame.quit()
            break

        # update simulation
        if not sim.paused:
            sim.step()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sim.step()

    # Lets move our lists to numpy array
    # first row contains times, second row contains positions
    pos_vs_times = np.vstack([sim.times, sim.positions])

    # Using matplotlib to plot simulation data
    plt.figure(1)
    plt.plot(pos_vs_times[0,:], pos_vs_times[1,:])
    plt.xlabel('Time (ms)')
    plt.ylabel('y position')
    plt.title('Height vs. Time')

    # velocity vs time data to plot
    vel_vs_times = np.vstack([sim.times, sim.velocities])

    plt.figure(2)
    plt.plot(vel_vs_times[0,:], vel_vs_times[1,:])
    plt.xlabel('Time (ms)')
    plt.ylabel('velocity')
    plt.title('Velocity vs. Time')

    # Writes to file if end of screen
    if end_of_screen:
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
    else:
        write_to_file(DATA_FILE, [pos_vs_times[1,:], vel_vs_times[1,:]])

    plt.show()

if __name__ == '__main__':
    main()
