# Created: 04/10/23
# Last edited: 31/10/23 - added matplotlib 3D scatter for graphics

import numpy as np                  # Used for vector calculations
import matplotlib.pyplot as plt     # Used for GUI
from math import sin, cos           # Used for trig calculations
from math import radians as rad     # Convert degrees to radians


# Calculates the magnitude of a vector
def mag(vector) -> float:
    total = sum(list(map(lambda x: x ** 2, vector)))  # Squares all the numbers and adds them together
    return total ** 0.5


# Classes for projectiles
class Projectile:
    def __init__(self, velocity: int | float, ele_angle: int | float, azi_angle: int | float, x: int | float,
                 y: int | float, z: int | float, gravity: int | float, **kwargs):
        self.u = velocity * np.array([cos(rad(ele_angle)) * cos(rad(azi_angle)),
                                      cos(rad(ele_angle)) * sin(rad(azi_angle)),
                                      sin(rad(ele_angle))])
        self.pos0 = np.array([x, y, z])  # Initial position
        self.pos = np.array([x, y, z])  # Current position
        self.g = np.array([0, 0, -gravity])  # Gravity vector

        self.max_h = 0  # Maximum height reached by projectile
        self.max_t = 0  # Time when max height reached

        self.time = 0
        self.landing_time = 0

        self.v = self.u  # Current velocity

        self.colour = kwargs.get("colour", "#FF0000")
        self.marker = kwargs.get("marker", "o")
        self.coords = [[x, y, z]]  # List storing all coordinates visited

    def calcDisplacement(self) -> float:
        s = self.pos - self.pos0
        return mag(s)

    def displayPath(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        n = (len(self.coords) // 20) + 1

        max_coords = max([max(row[0] for row in self.coords),  # Finds the max coordinate
                          max(row[1] for row in self.coords),
                          max(row[2] for row in self.coords)])

        ax.scatter([row[0] for row in self.coords][::n],
                   [row[1] for row in self.coords][::n],
                   [row[2] for row in self.coords][::n],
                   c=self.colour, marker=self.marker)

        ax.set_xlabel('X Axis / m')
        ax.set_ylabel('Y Axis / m')
        ax.set_zlabel('Z Axis / m')

        # Keeps the same scale with axes
        ax.set_xlim3d(0, max_coords)
        ax.set_ylim3d(0, max_coords)
        ax.set_zlim3d(0, max_coords)

        plt.show()


class ProjectileNoDrag(Projectile):
    def __init__(self, velocity: int | float, ele_angle: int | float, azi_angle: int | float, x: int | float,
                 y: int | float, z: int | float, gravity: int | float, **kwargs):
        super().__init__(velocity, ele_angle, azi_angle, x, y, z, gravity, **kwargs)

        self.max_t = -self.u[2] / self.g[2]
        self.max_h = self.position(self.max_t)[2]
        self.landing_time = self.max_t - ((self.u[2] ** 2 - 2 * self.g[2] * self.pos0[2]) ** 0.5) / self.g[2]
        self.landing_pos = self.position(self.landing_time)
        self.calcVelocity(self.landing_time)

    def position(self, time: float):
        return self.pos0 + self.u * time + 0.5 * self.g * time ** 2

    def move(self, dt: float):
        self.pos = self.position(self.time)
        self.time += dt
        self.coords.append([*self.pos])

    # Calculates the velocity of the projectile at a given time
    def calcVelocity(self, time):
        self.v = self.u + self.g * time


class ProjectileDrag(Projectile):
    def __init__(self, velocity: int | float, ele_angle: int | float, azi_angle: int | float, x: int | float,
                 y: int | float, z: int | float, gravity: int | float, mass: int | float, rho: int | float,
                 cd: int | float, area: int | float, **kwargs):
        super().__init__(velocity, ele_angle, azi_angle, x, y, z, gravity, **kwargs)
        self.m = mass  # Mass
        self.rho = rho  # Air density
        self.cd = cd  # Drag coefficient
        self.area = area  # Surface area

        self.p = self.m * self.v  # Momentum of the projectile

    def move(self, dt: float):
        # Checks if the projectile has risen
        if self.pos[2] > self.max_h:
            self.max_h = self.pos[2]
            self.max_t = self.time
        self.v = self.p / self.m
        # Calculates the net force on the projectile
        F_net = self.m * self.g - 0.5 * self.area * self.cd * self.rho * self.v * mag(self.v)
        self.p += F_net * dt
        self.pos += self.p * dt / self.m
        self.time += dt
        self.coords.append([*self.pos])


if __name__ == "__main__":
    proj_1 = ProjectileDrag(250, 30, 60, 0.0, 0.0, 50.0, 9.81, 20.0, 1.2, 0.07, 1)
    proj_2 = ProjectileNoDrag(250, 30, 60, 0.0, 0.0, 50.0, 9.81, colour="blue", marker="^")

    dt: float = 0.01

    for proj in (proj_1, proj_2):
        while proj.pos[2] >= 0:
            proj.move(dt)
        proj.displayPath()
