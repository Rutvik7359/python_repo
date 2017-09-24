import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
        self.pos = [0, 0]
        self.m = 1.0
        self.trace_x = 0
        self.trace_y = 0
        self.vx = 0
        self.vy = 0
        self.mass = 0

        self.f = 0.0001
        self.g = -9.8 # gravity acts downwards
        self.dt = 0.033 # 33 millisecond, which corresponds to 30 fps
        self.cur_time = 0

        self.paused = True 

    def f(self, t, state, arg1, arg2):
        print ("")
        
    def setup(self, speed, angle_degrees):
        self.trace_x = [self.pos[0]]
        self.trace_y = [self.pos[1]]

    def step(self):
        self.cur_time += self.dt

        # TO DO

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

def sim_to_screen(win_height, x, y):
    '''flipping y, since we want our y to increase as we move up'''
    x += 10
    y += 10

    return x, win_height - y

def main():

    # initializing pygame
    pygame.init()

    # top left corner is (0,0)
    win_width = 640
    win_height = 640
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('2D projectile motion')

    # setting up a sprite group, which will be drawn on the
    # screen
    my_sprite = MyCircle(RED, 5, 5)
    my_group = pygame.sprite.Group(my_sprite)

    # setting up simulation
    sim = Simulation()
    sim.setup(50., 45.)

    print ('--------------------------------')
    print ('Usage:')
    print ('Press (r) to start/resume simulation')
    print ('Press (p) to pause simulation')
    print ('Press (space) to step forward simulation when paused')
    print ('--------------------------------')

    while True:
        # 30 fps
        clock.tick(30)

        # update sprite x, y position using values
        # returned from the simulation
        my_sprite.rect.x, my_sprite.rect.y = sim_to_screen(win_height, sim.pos[0], sim.pos[1])

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
        else:
            pass

        # clear the background, and draw the sprites
        screen.fill(WHITE)
        my_group.update()
        my_group.draw(screen)
        pygame.display.flip()

        if sim.pos[1] <= -1.:
            pygame.quit()
            break

        # update simulation
        if not sim.paused:
            sim.step()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sim.step()

    plt.figure(1)
    plt.plot(sim.trace_x, sim.trace_y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.title('2D projectile trajectory')
    plt.show()


if __name__ == '__main__':
    main()
