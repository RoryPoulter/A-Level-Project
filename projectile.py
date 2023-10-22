# Created: 04/10/23
# Last edited: 22/10/23 - changed z as up

import numpy as np  # Used for vector calculations
from math import sin, cos  # Used for trig calculations
from math import radians as rad  # Convert degrees to radians


# Calculates the magnitude of a vector
def mag(vector) -> float:
    total = sum(list(map(lambda x: x ** 2, vector)))  # Squares all the numbers and adds them together
    return total ** 0.5


# Classes for projectiles
class Projectile:
    def __init__(self, velocity: int | float, ele_angle: int | float, azi_angle: int | float, x: int | float,
                 y: int | float, z: int | float, gravity: int | float):
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

    def calcDisplacement(self) -> float:
        s = self.pos - self.pos0
        return mag(s)


class ProjectileNoDrag(Projectile):
    def __init__(self, velocity: int | float, ele_angle: int | float, azi_angle: int | float, x: int | float,
                 y: int | float, z: int | float, gravity: int | float):
        super().__init__(velocity, ele_angle, azi_angle, x, y, z, gravity)

        self.max_t = -self.u[2] / self.g[2]
        self.max_h = self.position(self.max_t)[2]
        self.landing_time = self.max_t - ((self.u[2] ** 2 - 2 * self.g[2] * self.pos0[2]) ** 0.5) / self.g[2]
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
    def __init__(self, velocity: int | float, ele_angle: int | float, azi_angle: int | float, x: int | float,
                 y: int | float, z: int | float, gravity: int | float, mass: int | float, rho: int | float,
                 cd: int | float, area: int | float):
        super().__init__(velocity, ele_angle, azi_angle, x, y, z, gravity)
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


if __name__ == "__main__":
    dt = 0.01
    projectile = ProjectileNoDrag(20, 60, 0, 0, 10, 0, 10)
    while projectile.pos[2] >= 0:
        projectile.move(dt)
    projectile.calcVelocity()
    print(f"""Final position {projectile.landing_pos}
Landing time: {projectile.landing_time}s
Final velocity: {projectile.v}m/s
Displacement: {projectile.calcDisplacement()}m
Max height: {projectile.max_h}m
Time: {projectile.max_t}s\n""")

    projectile = ProjectileDrag(20, 60, 0, 0.0, 10.0, 0.0, 10.0, 10,
                                1.2, 0.47, 4.5)
    while projectile.pos[2] >= 0:
        projectile.move(dt)
    print(f"""Final position {projectile.pos}
Landing time: {projectile.time}s
Final velocity: {projectile.v}m/s
Displacement: {projectile.calcDisplacement()}m
Max height: {projectile.max_h}m
Time: {projectile.max_t}s""")
