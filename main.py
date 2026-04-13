from body import Body  
from physics import update_bodies  
import numpy as np  
import matplotlib.pyplot as plt  
  
sun_traj = []  
earth_traj = []  
moon_traj = []  
rocket_traj = []  
  
# Sun  
sun = Body(  
    "Sun",  
    1.989e30,  
    6.96e8,  
    [0, 0, 0],  
    [0, 0, 0],  
    fixed=True  
)  
#earth  
earth = Body(  
    "Earth",  
    5.972e24,  
    6.371e6,  
    [1.496e11, 0, 0],  
    [0, 29780, 0]  
)  
#Moon  
moon = Body(  
    "Moon",  
    7.35e22,  
    1.737e6,  
    earth.pos + np.array([384400000, 0, 0]),  
    [0, 0, 0]   # placeholder  
)  
#Rocket  
  
rocket = Body(  
    "Rocket",  
    1000,  
    10,  
    earth.pos + np.array([earth.radius + 400e3 , 0, 0]),  # 400 km altitude  
    earth.vel.copy()  
)  
bodies = [sun, earth, moon, rocket]  
  
#Earth rotates once per 24h: w=2π/T  
earth.angular_velocity = 2 * np.pi / (24 * 3600)  
moon.angular_velocity = 2 * np.pi / (27.3 * 24 * 3600)  



#compass of the earth
def get_plot_pos(body):
    rel = body.pos - earth.pos

    if earth_centered:
        cos_t = np.cos(-earth.theta)
        sin_t = np.sin(-earth.theta)

        x = rel[0] * cos_t - rel[1] * sin_t
        y = rel[0] * sin_t + rel[1] * cos_t

        return np.array([x, y, rel[2]])
    else:
        return body.pos
  
  
# vector from Earth to Moon  
r = moon.pos - earth.pos  
dist = np.linalg.norm(r)  
  
# orbital speed of Moon around Earth  
v_rel = np.sqrt(6.67430e-11 * earth.mass / dist)  
  
# perpendicular direction (VERY IMPORTANT)  
k = np.array([0, 0, 1])   # z-axis (orbit normal)  
direction = np.cross(k, r)  
direction = direction / np.linalg.norm(direction)  
  
# final velocity = Earth's velocity + relative orbit velocity  
moon.vel = earth.vel + direction * v_rel  
  
# vector from Earth to Rocket  
r_r = rocket.pos - earth.pos  
dist_r = np.linalg.norm(r_r)  
  
# orbital velocity magnitude  
v_r = np.sqrt(6.67430e-11 * earth.mass / dist_r)  
  
# perpendicular direction (same method as moon)  
k = np.array([0, 0, 1])  
dir_r = np.cross(k, r_r)  
dir_r = dir_r / np.linalg.norm(dir_r)  
  
# final velocity of rocket
omega = np.array([0, 0, earth.angular_velocity])
r_surface = rocket.pos - earth.pos

v_rot = np.cross(omega, r_surface)

rocket.vel = earth.vel + v_rot + dir_r * v_r
  
  
dt = 50  # 1050sec per step  
earth.theta = 0  
#Plotting  
plt.ion()  
fig = plt.figure()  
ax = fig.add_subplot(111)  
 
#center   
earth_centered = False  # toggle  , this will be placed by the gui software based on user's toggle.'
def on_key(event):
    global earth_centered
    if event.key == 't':
        earth_centered = not earth_centered

fig.canvas.mpl_connect('key_press_event', on_key)

#loop of position  
  
for step in range(10000):  
    earth.theta += earth.angular_velocity * dt  
    for _ in range(5):  
        update_bodies(bodies, dt)  
    max_points = 200000
    sun_traj.append(sun.pos.copy())  
    earth_traj.append(earth.pos.copy())  
    if len(earth_traj) > max_points:   
        earth_traj.pop(0)  
    moon_traj.append(moon.pos.copy())
    if len(moon_traj) > max_points:   
        moon_traj.pop(0)  
    rocket_traj.append(rocket.pos.copy())  
    if len(rocket_traj) > max_points:   
        rocket_traj.pop(0)  
          
          
    if step % 100 == 0:  
        ax.clear()  
          
        # plot bodies (XY projection)  
        scale = 20000  # adjust visually  
        #trajectories  
        def transform_traj(traj):
            transformed = []
            for p in traj:
                rel = p - earth.pos
        
                if earth_centered:
                    cos_t = np.cos(-earth.theta)
                    sin_t = np.sin(-earth.theta)
        
                    x = rel[0] * cos_t - rel[1] * sin_t
                    y = rel[0] * sin_t + rel[1] * cos_t
                else:
                    x, y = p[0], p[1]
        
                transformed.append((x, y))
            return transformed                

        ax.plot(*zip(*transform_traj(earth_traj)), color="deepskyblue")
        ax.plot(*zip(*transform_traj(moon_traj)), color="gray")
        ax.plot(*zip(*transform_traj(rocket_traj)), color="red")          
          
        def get_plot_pos(body):
            rel = body.pos - earth.pos
        
            if earth_centered:
                cos_t = np.cos(-earth.theta)
                sin_t = np.sin(-earth.theta)
        
                x = rel[0] * cos_t - rel[1] * sin_t
                y = rel[0] * sin_t + rel[1] * cos_t
        
                return np.array([x, y, rel[2]])
            else:
                return body.pos
        #scatters  
        if not earth_centered:
            p = get_plot_pos(sun)
            ax.scatter(p[0], p[1], s=sun.radius/scale, color="orange", label="Sun") 
        p = get_plot_pos(earth)  
        ax.scatter(p[0], p[1], s=earth.radius/scale,color= "deepskyblue", label="Earth")  
        p = get_plot_pos(moon)  
        ax.scatter(p[0], p[1], s=moon.radius/scale,color= "gray", label="Moon")  
        p = get_plot_pos(rocket)  
        ax.scatter(p[0], p[1], s=10,color= "red", label="Rocket")  
  
        if earth_centered:
            ax.set_xlim(-4.1e8, 4.1e8)
            ax.set_ylim(-4.1e8, 4.1e8)
        else:
            ax.set_xlim(-2e11, 2e11)
            ax.set_ylim(-2e11, 2e11)
        ax.legend(loc="upper left", markerscale=0.1)  
        plt.pause(0.001)  
  
