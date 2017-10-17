"""
author: Faisal Qureshi
email: faisal.qureshi@uoit.ca
website: http://www.vclab.ca
license: BSD
"""


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.integrate import ode

# Setup figure
fig = plt.figure(1)
ax = plt.axes(xlim=(0, 300), ylim=(-200, 1000))
plt.grid()
line, = ax.plot([], [], '-')
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
plt.title('Ball-Floor-Collision: Height vs. Time')
plt.xlabel('Time')
plt.ylabel('Height')


# Background for each function
def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text, 

# Called at each frame
def animate(i, ball):
    line.set_xdata(np.append(line.get_xdata(), ball.t))
    line.set_ydata(np.append(line.get_ydata(), ball.state[0]))
    time_text.set_text(time_template % ball.t)

    ball.update()
    return line, time_text, 

# Ball simulation - bouncing ball
class Ball:
    def __init__(self):

        # You don't need to change y, vy, g, dt, t and mass
        self.state = [400, -60]
        self.g = 9.8
        self.dt = 1.0
        self.t = 0
        self.mass = 1

        self.tol_distance = 10

        # We plan to use rk4
        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_initial_value(self.state, self.t)

    def f(self, t, y):
        return [y[1], -self.g]

    def is_collision(self, state):
        return state[0] <= 0

    def respond_to_collision(self, state, t):
        dt = self.dt
        s0 = self.state
        t0 = self.t
        dt_frac = self.dt

        new_state = state[:]

        while True:
            # if above
            if new_state[0] < 0:
                dt_frac /= 2
            elif new_state[0] > 0:
                dt_frac += dt_frac/2

            t = t0 + dt_frac
            self.solver.set_initial_value(s0, t0)
            new_state = self.solver.integrate(t)

            if (abs(new_state[0]) <= self.tol_distance):
                # Make sure above height is above 0
                if (new_state[0] > 0):
                    break

        return [0, -1*new_state[1]], t

    def update(self):
        new_state = self.solver.integrate(self.t + self.dt)

        # Collision detection
        if not self.is_collision(new_state):
            self.state = new_state
            self.t += self.dt 
        else:
            state_after_collision, collision_time = self.respond_to_collision(new_state, self.t+self.dt)
            self.state = state_after_collision
            self.t = collision_time
            self.solver.set_initial_value(self.state, self.t)

ball = Ball()

# blit=True - only re-draw the parts that have changed.
# repeat=False - stops when frame count reaches 999
# fargs=(ball,) - a tuple that can be used to pass extra arguments to animate function
anim = animation.FuncAnimation(fig, animate, fargs=(ball,), init_func=init, frames=300, interval=10, blit=True, repeat=False)
#plt.savefig('bouncing-ball-trace', format='png')

# Save the animation as an mp4.  For more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
# anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()