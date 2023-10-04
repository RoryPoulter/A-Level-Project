# Created: 04/10/23
# Last edited: 04/10/23

import numpy as np                  # Used for vector calculations
from math import sin, cos           # Used for trig calculations
from math import radians as rad     # Convert degrees to radians


# Calculates the magnitude of a vector
def mag(vector):
    total = sum(list(map(lambda x: x**2, vector)))
    return total**0.5


# Classes for projectiles
class Projectile:
    def __init__(self, u: float, ele_angle: float, azi_angle: float, x: int, y: int, z: int, g: float):
        self.u = u * np.array([cos(rad(ele_angle))*cos(rad(azi_angle)),
                               sin(rad(ele_angle)),
                               cos(rad(ele_angle))*sin(rad(azi_angle))])
        self.pos0 = np.array([x, y, z])
        self.pos = self.pos0
        self.g = np.array([0, -g, 0])

        self.max_h = 0
        self.max_t = 0

        self.time = 0
        self.landing_time = 0

        self.v = self.u

    def calcDisplacement(self):
        return mag(self.pos-self.pos0)


class ProjectileNoDrag(Projectile):
    def __init__(self, u: float, ele_angle: float, azi_angle: float, x: int, y: int, z: int, g: float):
        super().__init__(u, ele_angle, azi_angle, x, y, z, g)

        self.max_t = -self.u[1]/self.g[1]
        self.max_h = self.position(self.max_t)[1]
        self.landing_time = self.max_t - ((self.u[1]**2 - 2*self.g[1]*self.pos0[1])**0.5) / self.g[1]
        self.landing_pos = self.position(self.landing_time)

    def position(self, time: float):
        return self.pos0 + self.u * time + 0.5 * self.g * time ** 2

    def move(self, dt: float):
        self.pos = self.position(self.time)
        self.time += dt

    # Calculates the velocity of the projectile at a given time
    def calcVelocity(self):
        self.v = self.u + self.g * self.time


class ProjectileDrag(Projectile):
    def __init__(self, u: float, ele_angle: float, azi_angle: float, x: int, y: int, z: int, g: float, m: float,
                 rho: float, cd: float, a: float):
        super().__init__(u, ele_angle, azi_angle, x, y, z, g)
        self.m = m
        self.rho = rho
        self.cd = cd
        self.area = a

        self.p = self.m * self.v    # Momentum of the projectile

    def move(self, dt: float):
        # Checks if the projectile has risen
        if self.pos[1] > self.max_h:
            self.max_h = self.pos[1]
            self.max_t = self.time
        self.v = self.p / self.m
        # Calculates the net force on the projectile
        F_net = self.m*self.g - 0.5 * self.area * self.cd * self.rho * self.v * mag(self.v)
        self.p += F_net * dt
        self.pos += self.p * dt / self.m
        self.time += dt


if __name__ == "__main__":
    projectile = ProjectileNoDrag(20, 50, 45, 0, 0, 0, 9.81)
