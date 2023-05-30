import numpy
from random import uniform, randrange
from math import sqrt

class particle:
    
    def __init__(self, x: float, y: float, x_vel: float, y_vel: float, mass: float, radius: float, collisionless: bool, colour: tuple) -> None:
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        self.radius = radius
        self.collisionless = collisionless
        self.colour = colour

    def update_position(self, bounds, particles, delta):
        if self.collisionless: self.__collisionless_move(bounds, delta)
        else: self.__collision_move(bounds, particles, delta)

    def __collisionless_move(self, bounds, delta):
        if self.x - self.radius <= bounds[0] or self.x + self.radius >= bounds[1]:
            self.x_vel = -self.x_vel
        if self.y - self.radius <= bounds[2] or self.y + self.radius >= bounds[3]:
            self.y_vel = -self.y_vel
        dx = (self.x_vel / 1000) * delta
        dy = (self.y_vel / 1000) * delta
        self.x += dx
        self.y += dy

    def __collision_move(self, bounds, particles, delta):
        #TODO
        pass
        
        

def generate_gas(num_particles: int, bounds: list, average_vel: float, collisionless: bool, colour: tuple, highlight: tuple, mass=5, radius=5):
    bounds[0] += radius
    bounds[1] -= radius
    bounds[2] += radius
    bounds[3] -= radius

    xy_locs = []

    x_loc = bounds[0] + 2 * radius
    while x_loc < bounds[1] - 2 * radius:
        y_loc = bounds[2] + 2 * radius
        while y_loc < bounds[3] - 2 * radius:
            xy_locs.append((x_loc, y_loc))
            y_loc += 2 * radius
        x_loc += 2 * radius

    if len(xy_locs) < num_particles: num_particles = len(xy_locs)
    print(f'Number of particles: {num_particles}')

    velocities = numpy.random.normal(average_vel, 0.05 * average_vel, num_particles)
    
    particles = []
    for i in range(num_particles):
        x_vel = uniform(-velocities[i], velocities[i])
        y_vel = randrange(-1, 2, 2) * (sqrt(velocities[i]**2 - x_vel**2))
        x = xy_locs[i][0]
        y = xy_locs[i][1]
        c = highlight if i == num_particles // 2 else colour
        p = particle(x, y, x_vel, y_vel, mass, radius, collisionless, c)
        particles.append(p)

    return particles