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

    def update_position(self, bounds, delta):
        if self.x - self.radius <= bounds[0]:
            self.x_vel = -self.x_vel
            self.x = bounds[0] + self.radius
        elif self.x + self.radius >= bounds[1]:
            self.x_vel = -self.x_vel
            self.x = bounds[1] - self.radius
        if self.y - self.radius <= bounds[2]:
            self.y_vel = -self.y_vel
            self.y = bounds[2] + self.radius
        elif self.y + self.radius >= bounds[3]:
            self.y_vel = -self.y_vel
            self.y = bounds[3] - self.radius
        dx = (self.x_vel / 1000) * delta
        dy = (self.y_vel / 1000) * delta
        self.x += dx
        self.y += dy
        
    def collides_with(self, p):
        return sqrt((self.x - p.x)**2 + (self.y - p.y)**2) <= self.radius + p.radius
        

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

def collide(p1: particle, p2: particle):
    col_norm = [p1.x - p2.x, p1.y - p2.y]
    col_norm_l = sqrt(col_norm[0]**2 + col_norm[1]**2)
    col_norm = [col_norm[0] / col_norm_l, col_norm[1] / col_norm_l]
    
    v1 = [p1.x_vel, p1.y_vel]
    v1_dot_cn = v1[0] * col_norm[0] + v1[1] * col_norm[1]
    v1col = [col_norm[0] * v1_dot_cn, col_norm[1] * v1_dot_cn]
    v1rem = [v1[0] - v1col[0], v1[1] - v1col[1]]
    
    v2 = [p2.x_vel, p2.y_vel]
    v2_dot_cn = v2[0] * col_norm[0] + v2[1] * col_norm[1]
    v2col = [col_norm[0] * v2_dot_cn, col_norm[1] * v2_dot_cn]
    v2rem = [v2[0] - v2col[0], v2[1] - v2col[1]]
    
    v1length = sqrt(v1col[0]**2 + v1col[1]**2) * (v1_dot_cn / abs(v1_dot_cn))
    v2length = sqrt(v2col[0]**2 + v2col[1]**2) * (v2_dot_cn / abs(v2_dot_cn))
    
    commonvel = 2 * (p1.mass * v1length + p2.mass * v2length) / (p1.mass + p2.mass)
    
    v1len_aft = commonvel - v1length
    v2len_aft = commonvel - v2length
    
    v1col = [v1col[0] * (v1len_aft / v1length), v1col[1] * (v1len_aft / v1length)]
    v2col = [v2col[0] * (v2len_aft / v2length), v2col[1] * (v2len_aft / v2length)]
    
    p1.x_vel, p1.y_vel = (v1col[0] + v1rem[0], v1col[1] + v1rem[1])
    p2.x_vel, p2.y_vel = (v2col[0] + v2rem[0], v2col[1] + v2rem[1])
    
    dpos = [p2.x - p1.x, p2.y - p1.y]
    dpos_mag = sqrt(dpos[0]**2 + dpos[1]**2)
    dpos_unit = [dpos[0] / dpos_mag, dpos[1] / dpos_mag]
    
    dp = [((p1.radius + p2.radius - dpos_mag) / 2) * dpos_unit[0], ((p1.radius + p2.radius - dpos_mag) / 2) * dpos_unit[1]]
    
    p1.x -= dp[0]
    p1.y -= dp[1]
    p2.x += dp[0]
    p2.y += dp[1]
    