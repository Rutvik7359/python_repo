import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode

rk4 = False

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# image files
EARTH_IMAGE = 'earth.png'
MOON_IMAGE = 'moon.png'

# constants
G = 6.674e-11 # N kg-2 m^2
Earth_Mass = 5.972e24 # kg
Moon_Mass = 7.34767309e22 # kg
Distance = 384400000. # m


# clock object that ensure that animation has the same
# on all machines, regardless of the actual machine speed.
clock = pygame.time.Clock()

# in case we need to load an image
def load_image(name):
    image = pygame.image.load(name)
    return image

class HeavenlyBody(pygame.sprite.Sprite):
    
    def __init__(self, name, mass, color=WHITE, radius=0, imagefile=None):
        pygame.sprite.Sprite.__init__(self)

        if imagefile:
            self.image = load_image(imagefile)
            self.image = pygame.transform.scale(self.image, (int(radius*2), int(radius*2)))
        else:
            self.image = pygame.Surface([radius*2, radius*2])
            self.image.fill(BLACK)
            pygame.draw.circle(self.image, color, (radius, radius), radius, radius)

        self.rect = self.image.get_rect()
        self.pos = np.array([0,0])
        self.vel = np.array([0,0])
        self.mass = mass
        self.radius = radius
        self.name = name
        self.G = G
        self.distances = []
        self.cur_time = 0
        self.other_pos = np.array([0,0])
        self.damp = 0.01

        if rk4:
            self.solver = ode(self.f)
            self.solver.set_integrator('dop853')

    def f(self, t, state):
        f, r = self.get_force_and_rad(self.other_pos, state[0:2])

        dx = state[2] - state[2]*self.damp# velocity in x dir
        dy = state[3] - state[3]*self.damp # velocity in y dir
        dvx = f[0]/self.mass
        dvy = f[1]/self.mass

        return [dx, dy, dvx, dvy]

    def set_pos(self, pos):
        self.pos = np.array(pos)

    def set_vel(self, vel):
        self.vel = np.array(vel)
        if rk4:
            self.solver.set_initial_value([self.pos[0], self.pos[1], self.vel[0], self.vel[1]], self.cur_time)

    def update1(self, objects, dt):
        force = np.array([0,0])
        for o in objects:
            if o != self.name:
                other = objects[o]

                f, r= self.get_force_and_rad(other.pos, self.pos)

                print 'Force on', self.name, ' from', other.name, '=', f
                print 'Mass-1', self.mass, 'mass-2', other.mass
                print 'G', self.G
                print 'Distance', r
                print 'Vel', self.vel

                if rk4:
                    if self.solver.successful():
                        self.cur_time += dt

                        self.solver.integrate(self.cur_time)
                        self.pos = self.solver.y[0:2]
                        self.vel = self.solver.y[2:4]
                else:
                    new_vel = self.vel + dt * f / self.mass
                    new_pos = self.pos + dt * self.vel
                    self.vel = new_vel
                    self.pos = new_pos

                if self.name == 'earth':
                    self.distances.append(r)

    def get_force_and_rad(self, other_pos, pos):
        d = (other_pos - pos)
        r = np.linalg.norm(d)
        u = d / r
        f = u * G * Earth_Mass * Moon_Mass / (r*r)

        return f, r

class Universe:
    def __init__(self):
        self.w, self.h = 2.6*Distance, 2.6*Distance 
        self.objects_dict = {}
        self.objects = pygame.sprite.Group()
        self.dt = 1000.0

    def add_body(self, body):
        self.objects_dict[body.name] = body
        self.objects.add(body)

    def to_screen(self, pos):
        return [int((pos[0] + 1.3*Distance)*640/self.w), int((pos[1] + 1.3*Distance)*640./self.h)]

    def update(self):

        for o in self.objects_dict:
            # Comput positions for screen
            obj = self.objects_dict[o]
            if obj.name == 'moon':
                obj.other_pos = self.objects_dict['earth'].pos
            else:
                obj.other_pos = self.objects_dict['moon'].pos

            obj.update1(self.objects_dict, self.dt)
            p = self.to_screen(obj.pos)

            if False: # Set this to True to print the following values
                print 'Name', obj.name
                print 'Position in simulation space', obj.pos
                print 'Position on screen', p

            # Update sprite locations
            obj.rect.x, obj.rect.y = p[0]-obj.radius, p[1]-obj.radius
        self.objects.update()

    def draw(self, screen):
        self.objects.draw(screen)

def main():

    print 'Press q to quit'

    # Initializing pygame
    pygame.init()
    win_width = 640
    win_height = 640
    screen = pygame.display.set_mode((win_width, win_height))  # Top left corner is (0,0)
    pygame.display.set_caption('Heavenly Bodies')

    # Create a Universe object, which will hold our heavenly bodies (planets, stars, moons, etc.)
    universe = Universe()

    earth = HeavenlyBody('earth', Earth_Mass, radius=32, imagefile=EARTH_IMAGE)
    earth.set_pos([0, 0])
    earth.set_vel([0, 0])
    moon = HeavenlyBody('moon', Moon_Mass, WHITE, radius=10, imagefile=MOON_IMAGE)
    moon.set_pos([int(Distance), 0])
    moon.set_vel([0, 1000])

    universe.add_body(earth)
    universe.add_body(moon)

    total_frames = 100000
    iter_per_frame = 10

    frame = 0
    while frame < total_frames:
        print 'Frame number', frame        

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.pause()
            sys.exit(0)
        else:
            pass

        universe.update()
        if frame % iter_per_frame == 0:
            screen.fill(BLACK) # clear the background
            universe.draw(screen)
            pygame.display.flip()
        frame += 1

    pygame.quit()


if __name__ == '__main__':
    main()
