import numpy as np

G = 6.67430e-11

def compute_acceleration(body, bodies):
    acc = np.zeros(3)

    for other in bodies:
        if other is body:
            continue
        
        r_vec = other.pos - body.pos
        r = np.linalg.norm(r_vec)

        if r == 0:
            continue

        acc += G * other.mass * r_vec / r**3

    return acc

def update_bodies(bodies, dt):
    accelerations = {}

    # compute all accelerations first
    for body in bodies:
        if not body.fixed:
            accelerations[body] = compute_acceleration(body, bodies)

    # then update
    for body in bodies:
        if not body.fixed:
            body.vel += accelerations[body] * dt
            body.pos += body.vel * dt

