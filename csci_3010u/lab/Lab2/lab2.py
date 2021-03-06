import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.integrate import ode

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DEFAULT_ANGLE = 45.
DEFAULT_SPEED = 50.

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
        self.vel = [0, 0]
        self.fric = 0.0001 # friction coefficient
        self.g = -9.8 # gravity acts downwards
        self.dt = 0.033 # 33 millisecond, which corresponds to 30 fps
        self.cur_time = 0

        self.paused = True 

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_f_params(self.fric, self.g)

    def f(self, t, state, arg1, arg2):
        dx  = state[2]
        dy  = state[3]
        dvx = - state[2] * arg1
        dvy = arg2 - state[3] * arg1
        return [dx, dy, dvx, dvy]  
        
    def setup(self, speed, angle_degrees):
        self.vel[0] = speed*math.cos(angle_degrees)
        self.vel[1] = speed*math.sin(angle_degrees)
        self.cur_time = 0
        self.solver.set_initial_value([self.pos[0],self.pos[1], self.vel[0], self.vel[1]], self.cur_time)
        self.trace_x = [self.pos[0]]
        self.trace_y = [self.pos[1]]

    def step(self):
        self.cur_time += self.dt

        if self.solver.successful():
            self.solver.integrate(self.cur_time)
            self.pos = self.solver.y[0:2]
            self.vel = self.solver.y[2:4]
            self.trace_x.append(self.pos[0])
            self.trace_y.append(self.pos[1])        

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

def sim_to_screen(win_height, x, y):
    '''flipping y, since we want our y to increase as we move up'''
    x += 10
    y += 10

    return x, win_height - y

def deg_to_rad(deg):
    return math.pi*deg/180

def usage():
    print ('--------------------------------')
    print ('Usage:')
    print ('--------------------------------')
    print ('python lab2.py <angle(degrees)> <speed>')
    print ('or')
    print ('python lab2.py')
    print ('(Angle default: 45°)')
    print ('(Speed default: 50)')
    print ('--------------------------------')

def main():

    # Error checking command line args and setting angle
    num_args = len(sys.argv) - 1
    if num_args == 2:
        angle = float(sys.argv[1])
        speed = float(sys.argv[2])
    elif num_args == 1 or num_args > 2:
        usage()
        sys.exit(0)
    else:
        angle = DEFAULT_ANGLE
        speed = DEFAULT_SPEED

    # initializing pygame
    pygame.init()

    # top left corner is (0,0)
    win_width = 640
    win_height = 480
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('2D projectile motion')

    # setting up a sprite group, which will be drawn on the
    # screen
    my_sprite = MyCircle(RED, 10, 10)
    my_group = pygame.sprite.Group(my_sprite)

    # setting up simulation
    sim = Simulation()

    sim.setup(speed, deg_to_rad(angle))

    print ('Usage during simulation:')
    print ('--------------------------------')
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
    #plt.show()

    print("Angle:       " + str(angle) + "°")
    print("Speed:       " + str(speed))
    print("Distance(x): " + str(sim.trace_x[-1]))
    
    #with open("out.txt", "a") as myfile:
    #    myfile.write(str(angle) + ", " + str(speed) + ", " + str(sim.trace_x[-1]) + "\n")

if __name__ == '__main__':
    main()
