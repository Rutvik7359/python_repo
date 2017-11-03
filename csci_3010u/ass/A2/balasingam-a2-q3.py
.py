import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.integrate import ode
import os

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIN_HEIGHT = 500
WIN_WIDTH = 500
WALLS = ["left", "right", "top", "bottom"]


def normalize(v):
    return v / np.linalg.norm(v)

class Disk2D(pygame.sprite.Sprite):
    
    def __init__(self, imgfile, radius, mass=1.0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(imgfile)
        self.image = pygame.transform.smoothscale(self.image, (radius*2, radius*2)) 
        self.state = [0, 0, 0, 0]
        self.mass = mass
        self.t = 0
        self.radius = radius

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_initial_value(self.state, self.t)

    def f(self, t, y):
        return [y[2], y[3], 0, 0]

    def set_pos(self, pos):
        self.state[0:2] = pos
        self.solver.set_initial_value(self.state, self.t)
        return self

    def set_vel(self, vel):
        self.state[2:] = vel
        self.solver.set_initial_value(self.state, self.t)
        return self

    def update(self, dt):
        self.t += dt
        self.state = self.solver.integrate(self.t)

    def move_by(self, delta):
        self.state[0:2] = np.add(self.pos, delta)
        return self

    def draw(self, surface):
        rect = self.image.get_rect()
        rect.center = (self.state[0], WIN_HEIGHT-self.state[1])
        surface.blit(self.image, rect)

    def pprint(self):
        print 'Disk', self.state

class World:

    def __init__(self):
        self.disks = []
        self.e = 1. # Coefficient of restitution

    def add(self, imgfile, radius, mass=1.0):
        disk = Disk2D(imgfile, radius, mass)
        self.disks.append(disk)
        return disk

    def pprint(self):
        print '#disks', len(self.disks)
        for d in self.disks:
            d.pprint()

    def draw(self, screen):
        for d in self.disks:
            d.draw(screen)

    def update(self, dt):

        self.check_for_collision()

        for d in self.disks:
            d.update(dt)

    
    def check_for_collision(self):
        for i in range(0, len(self.disks)):

            # Check disk-wall collisions first
            for k in range(0, len(WALLS)):
                self.compute_collision_response(i, -1, WALLS[k])

            # Check disk-disk collisions next
            for j in range(i+1, len(self.disks)):
                if i == j:
                    continue

                if self.compute_collision_response(i, j):
                    break


    def compute_collision_response(self, i, j, wall=""):
        pos_i = np.array(self.disks[i].state[0:2])
        mass_i = self.disks[i].mass

        # If checking collision with wall
        if j == -1:
            if wall == "left":
                pos_j = [0, pos_i[1]]
            elif wall == "right":
                pos_j = [WIN_WIDTH, pos_i[1]]
            elif wall == "top":
                pos_j = [pos_i[0], WIN_HEIGHT]
            else:
                pos_j = [pos_i[0], 0]

            radius_j = 0
            vel_j = [0, 0]
            mass_denom = (1./mass_i)

        # If checking collision with another disk    
        else:
            pos_j = np.array(self.disks[j].state[0:2])
            vel_j = self.disks[j].state[2:]
            radius_j = self.disks[j].radius
            mass_j = self.disks[j].mass
            mass_denom = (1./mass_i) + (1./mass_j)

        diff_pos = pos_i - pos_j
        dist = np.sqrt(np.sum(diff_pos**2))

        # Check if distance between objects is less than or equal to object 
        # radiuses. If so, then collision
        if dist <= (self.disks[i].radius + radius_j):
            vel_i = np.array(self.disks[i].state[2:])

            relative_vel_ij = vel_i - vel_j
            n_ij = normalize(diff_pos)

            # Set resulting velocity/velocities
            if np.dot(relative_vel_ij, n_ij) < 0:
                J = -(1+self.e) * np.dot(relative_vel_ij, n_ij) / mass_denom

                vel_i_aftercollision = vel_i + n_ij * J / mass_i
                self.disks[i].set_vel(vel_i_aftercollision)

                if j != -1:
                    vel_j_aftercollision = vel_j - n_ij * J / mass_j
                    self.disks[j].set_vel(vel_j_aftercollision)

                return True
        return False


def main():

   # initializing pygame
    pygame.init()

    clock = pygame.time.Clock()

    # top left corner is (0,0)
    win_width = WIN_WIDTH
    win_height = WIN_HEIGHT
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('Disk-Disk collisions')


    # Setting up random variables
    # -------------------------------------------------------------------------
    pos = []
    vel = []
    rad = []
    mass = []
    for i in range(0, 10):
        # random radiuses
        rad.append(int(100.*random.uniform(0.1, 0.2)))
        
        # random positions
        pos.append(random.uniform(0 + rad[i], WIN_WIDTH - rad[i]))
        pos.append(random.uniform(0 + rad[i], WIN_HEIGHT - rad[i]))

        # random velocities
        vel_mag = 0
        while vel_mag == 0:
            vel_mag = random.uniform(0, 1000)

        x_sign = random.choice([-1, 1])
        y_sign = random.choice([-1, 1])

        velx = x_sign*random.uniform(0, 1)*vel_mag
        vely = y_sign*np.sqrt(vel_mag**2 - velx**2)
        vel.append(velx)
        vel.append(vely)

        # random masses
        mass.append(random.uniform(1, 5))
    # -------------------------------------------------------------------------


    # Setting up disks
    # -------------------------------------------------------------------------
    disk_img = []
    for img_name in os.listdir("disk_images/"):
        disk_img.append(os.path.join("disk_images", img_name))

    world = World()

    for i in range(0, len(disk_img)):
        world.add(disk_img[i], rad[i], mass[i]).set_pos(pos[i:i+2]).set_vel(vel[i:i+2])
    # -------------------------------------------------------------------------


    dt = 0.01

    while True:
        # 30 fps
        clock.tick(30)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
        else:
            pass

        # Clear the background, and draw the sprites
        screen.fill(WHITE)
        world.draw(screen)
        world.update(dt)

        pygame.display.update()

if __name__ == '__main__':
    main()
