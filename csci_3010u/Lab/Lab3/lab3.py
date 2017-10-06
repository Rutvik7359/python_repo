import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode

USE_RK4 = True
MAKE_STABLE = True

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
EARTH_MASS = 5.972e24 # kg
MOON_MASS = 7.34767309e22 # kg
DISTANCE = 384400000. # m
INITIAL_EARTH_POS = np.array([0, 0])
INITIAL_MOON_POS = np.array([int(DISTANCE), 0])
INITIAL_MOON_VELOCITY = np.array([0, 1000])
TIME_STEP = 1000.0

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
        self.other_mass = 0
        self.damp = 0.01

        if USE_RK4:
            self.solver = ode(self.f)
            self.solver.set_integrator('dop853')

    def f(self, t, state):
        f, r = self.get_force_and_rad(self.other_pos, state[0:2])

        dx, dy = state[2:4] #velocity
        dvx, dvy = f/self.mass

        return [dx, dy, dvx, dvy]

    def setup(self, pos, vel=np.array([0,0])):
        self.set_pos(pos)
        self.set_vel(vel)

        if USE_RK4:
            self.solver.set_initial_value([self.pos[0], self.pos[1], self.vel[0], self.vel[1]], self.cur_time)

    def set_pos(self, pos):
        self.pos = np.array(pos)

    def set_vel(self, vel):
        if MAKE_STABLE and self.name == 'moon':
            self.other_mass = EARTH_MASS
            self.other_pos = INITIAL_EARTH_POS

            _, r = self.get_force_and_rad(self.other_pos, self.pos)

            # derive velocity from making centrifugal force and gravitational force equal
            self.vel = np.array([0, np.sqrt(self.G*self.other_mass/r)])
        else:    
            self.vel = np.array(vel)

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

                if USE_RK4:
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
        f = u * G * EARTH_MASS * MOON_MASS / (r*r)

        return f, r


class Universe:
    def __init__(self):
        self.w, self.h = 2.6*DISTANCE, 2.6*DISTANCE 
        self.objects_dict = {}
        self.objects = pygame.sprite.Group()
        self.dt = TIME_STEP
        self.paused = False

    def add_body(self, body):
        self.objects_dict[body.name] = body
        self.objects.add(body)

    def to_screen(self, pos):
        return [int((pos[0] + 1.3*DISTANCE)*640/self.w), int((pos[1] + 1.3*DISTANCE)*640./self.h)]

    def update(self):
        for o in self.objects_dict:
            # Comput positions for screen
            obj = self.objects_dict[o]

            if obj.name == 'moon':
                other = self.objects_dict['earth']
            else:
                other = self.objects_dict['moon']
            obj.other_pos = other.pos

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

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False


def main():
    print 'Press q to quit'
    print 'Press p to pause'
    print 'Press r to resume'

    # Initializing pygame
    pygame.init()
    win_width = 640
    win_height = 640
    screen = pygame.display.set_mode((win_width, win_height))  # Top left corner is (0,0)
    pygame.display.set_caption('Heavenly Bodies')

    # Create a Universe object, which will hold our heavenly bodies (planets, stars, moons, etc.)
    universe = Universe()

    earth = HeavenlyBody('earth', EARTH_MASS, radius=32, imagefile=EARTH_IMAGE)
    earth.setup(INITIAL_EARTH_POS)
    moon = HeavenlyBody('moon', MOON_MASS, WHITE, radius=10, imagefile=MOON_IMAGE)
    moon.setup(INITIAL_MOON_POS, INITIAL_MOON_VELOCITY)

    universe.add_body(earth)
    universe.add_body(moon)

    total_frames = 100000
    iter_per_frame = 10

    frame = 0
    while frame < total_frames:  
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            universe.pause()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            universe.resume()
            continue
        else:
            pass

        if not universe.paused:
            print 'Frame number', frame 
            universe.update()
            if frame % iter_per_frame == 0:
                screen.fill(BLACK) # clear the background
                universe.draw(screen)
                pygame.display.flip()
            frame += 1

    pygame.quit()


if __name__ == '__main__':
    main()
