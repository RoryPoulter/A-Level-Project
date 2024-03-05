# Created: 04/10/23
# Last edited: 08/12/23 - improved documentation

import numpy as np                  # Used for vector calculations
from math import sin, cos           # Used for trig calculations
from math import radians as rad     # Convert degrees to radians


def mag(vector):
    """
    Calculates the magnitude of a vector.
    :param vector: (Iterable) The nth dimensional vector
    :return: a float representing the magnitude of the vector
    :rtype: float
    """
    total = sum(list(map(lambda x: x ** 2, vector)))  # Squares all the numbers and adds them together
    return total ** 0.5


# Classes for projectiles
class Projectile:
    def __init__(self, velocity, ele_angle, azi_angle, x, y, z, gravity, **kwargs):
        """
        Creates an instance of the object
        :param velocity: The magnitude of the initial velocity
        :type velocity: float | int
        :param ele_angle: The elevation angle
        :type ele_angle: float | int
        :param azi_angle: The azimuth angle
        :type azi_angle: float | int
        :param x: The initial x coordinate
        :type x: float | int
        :param y: The initial y coordinate
        :type y: float | int
        :param z: The initial z coordinate (height)
        :type z: float | int
        :param gravity: The magnitude of acceleration due to gravity
        :type gravity: float | int
        :param kwargs: Appearance options for the scatter graph
        """
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

    def calcDisplacement(self):
        """
        Calculates the displacement of the projectile
        :return: the magnitude of the displacement
        :rtype: float
        """
        s = self.pos - self.pos0
        return mag(s)

    def displayPath(self, fig):
        """
        Plots the flight path on a 3D scatter graph
        :param fig: Matplotlib figure
        :return: Returns the Matplotlib subplot
        """
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

        return ax


class ProjectileNoDrag(Projectile):
    def __init__(self, velocity, ele_angle, azi_angle, x, y, z, gravity, **kwargs):
        """
        Creates an instance of the object
        :param velocity: The magnitude of the initial velocity
        :type velocity: float | int
        :param ele_angle: The elevation angle
        :type ele_angle: float | int
        :param azi_angle: The azimuth angle
        :type azi_angle: float | int
        :param x: The initial x coordinate
        :type x: float | int
        :param y: The initial y coordinate
        :type y: float | int
        :param z: The initial z coordinate (height)
        :type z: float | int
        :param gravity: The magnitude of acceleration due to gravity
        :type gravity: float | int
        :param kwargs: Appearance options for the scatter graph
        """
        super().__init__(velocity, ele_angle, azi_angle, x, y, z, gravity, **kwargs)

        self.max_t = -self.u[2] / self.g[2]
        self.max_h = self.position(self.max_t)[2]
        self.landing_time = self.max_t - ((self.u[2] ** 2 - 2 * self.g[2] * self.pos0[2]) ** 0.5) / self.g[2]
        self.landing_pos = self.position(self.landing_time)
        self.calcVelocity(self.landing_time)

    def position(self, time):
        """
        Calculates the position of the projectile at a given time
        :param time: the current time
        :type time: float | int
        :return: the current position
        """
        return self.pos0 + self.u * time + 0.5 * self.g * time ** 2

    def move(self, dt):
        """
        Updates the position and time
        :param dt: the interval between updating position
        :type dt: float
        """
        self.pos = self.position(self.time)
        self.time += dt
        self.coords.append([*self.pos])

    def calcVelocity(self, time):
        """
        Calculates the velocity at a given time
        :param time: the time since projection
        :type time: float
        """
        self.v = self.u + self.g * time


class ProjectileDrag(Projectile):
    def __init__(self, velocity, ele_angle, azi_angle, x, y, z, gravity, mass, air_density, drag_coefficient, area,
                 **kwargs):
        """
        Creates an instance of the object
        :param velocity: The magnitude of the initial velocity
        :type velocity: float | int
        :param ele_angle: The elevation angle
        :type ele_angle: float | int
        :param azi_angle: The azimuth angle
        :type azi_angle: float | int
        :param x: The initial x coordinate
        :type x: float | int
        :param y: The initial y coordinate
        :type y: float | int
        :param z: The initial z coordinate (height)
        :type z: float | int
        :param gravity: The magnitude of acceleration due to gravity
        :type gravity: float | int
        :param mass: The mass of the projectile
        :type mass: float | int
        :param air_density: The air density of the medium
        :type air_density: float | int
        :param drag_coefficient: The drag coefficient of the projectile
        :type drag_coefficient: float | int
        :param area: The surface area of the projectile
        :type area: float | int
        :param kwargs: Appearance options for the scatter graph
        """
        super().__init__(velocity, ele_angle, azi_angle, x, y, z, gravity, **kwargs)
        self.m = mass  # Mass
        self.rho = air_density  # Air density
        self.cd = drag_coefficient  # Drag coefficient
        self.area = area  # Surface area

        self.p = self.m * self.v  # Momentum of the projectile

    def move(self, dt):
        """
        Updates the position and time
        :param dt: the interval between updating position
        :type dt: float
        """
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


def compare_paths(projectile_1, projectile_2, fig):
    """
    Plots the flight paths of two projectiles on one scatter graph
    :param projectile_1: The 1st projectile object
    :type projectile_1: Projectile
    :param projectile_2: The 2nd projectile object
    :type projectile_2: Projectile
    :param fig: Matplotlib figure
    :return: Matplotlib subplot
    """
    ax = fig.add_subplot(111, projection='3d')

    for projectile in (projectile_1, projectile_2):
        n = (len(projectile.coords) // 20) + 1
        ax.scatter([row[0] for row in projectile.coords][::n],
                   [row[1] for row in projectile.coords][::n],
                   [row[2] for row in projectile.coords][::n],
                   c=projectile.colour, marker=projectile.marker)

    max_coords_1 = max([max(row[0] for row in projectile_1.coords),
                        max(row[1] for row in projectile_1.coords),
                        max(row[2] for row in projectile_1.coords)])

    max_coords_2 = max([max(row[0] for row in projectile_2.coords),
                        max(row[1] for row in projectile_2.coords),
                        max(row[2] for row in projectile_2.coords)])

    max_coords = max(max_coords_1, max_coords_2)

    ax.set_xlabel('X Axis / m')
    ax.set_ylabel('Y Axis / m')
    ax.set_zlabel('Z Axis / m')

    # Keeps the same scale with axes
    ax.set_xlim3d(0, max_coords)
    ax.set_ylim3d(0, max_coords)
    ax.set_zlim3d(0, max_coords)

    return ax
