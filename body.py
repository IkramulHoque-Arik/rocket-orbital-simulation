import numpy as np

class Body:
    def __init__(self, name, mass, radius, position, velocity, fixed=False):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.pos = np.array(position, dtype=float)  # now [x, y, z]
        self.vel = np.array(velocity, dtype=float)  # now [vx, vy, vz]
        self.fixed = fixed

        # rotational properties (for future GUI)
        self.rotation_angle = 0.0
        self.angular_velocity = 0.0

#

def update_bodies(bodies, dt):
    accelerations = {}

    for body in bodies:
        if not body.fixed:
            accelerations[body] = compute_acceleration(body, bodies)

    for body in bodies:
        if not body.fixed:
            body.vel += accelerations[body] * dt
            body.pos += body.vel * dt

            # rotation update
            body.rotation_angle += body.angular_velocity * dt


