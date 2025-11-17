import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

visual_lim = 80

class vehicle_struct:

    def __init__(self, states, idx):
        self.x = states[0, idx]
        self.y = 0
        self.theta = np.pi/2
        self.kappa = 0
        self.v = 0
        self.a = 0


def minmax(vec):
    return np.array([min(vec), max(vec)])


def plot_2d():
    artist_obj_list = []

    fig, ax = plt.subplots(figsize=(12, 4))
    ax = fig.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.xlabel('x (meter)')
    ax.set_yticks([])
    #plt.ylabel('y (meter)')
    plt.grid()
    plt.xlim(0, visual_lim)
    plt.ylim(-5, 5)
    fig.tight_layout()

    return fig, ax, artist_obj_list


def plot_vehicle_state(ax, s, **kwargs):
    artist_obj_list = []

    # rotation, translation
    ct = np.cos(s.theta)
    st = np.sin(s.theta)
    R = np.array([[ct, st],
                  [-st, ct]])
    T = np.array([s.x, s.y])

    slong = 4.5  # longitudinal size(meter)
    slat = 2.  # lateral size(meter)

    if 'color' in kwargs:
        artist_obj_list.append(box_in_frame(ax, 0., 0., slat, slong, R, T, **kwargs))  # car outset
        artist_obj_list.append(
            box_in_frame(ax, 0., slong * .05, slat * .8, slong * .2, R, T, **kwargs))  # front windshield
        artist_obj_list.append(
            box_in_frame(ax, 0., slong * -.25, slat * .8, slong * .15, R, T, **kwargs))  # back window
    else:
        artist_obj_list.append(
            box_in_frame(ax, 0., 0., slat, slong, R, T, color='black', label='Vehicle', **kwargs))  # car outset
        artist_obj_list.append(
            box_in_frame(ax, 0., slong * .05, slat * .8, slong * .2, R, T, color='black', **kwargs))  # front windshield
        artist_obj_list.append(
            box_in_frame(ax, 0., slong * -.25, slat * .8, slong * .15, R, T, color='black', **kwargs))  # back window

    # wheel angle
    kappa_mult = 1
    kct = np.cos(s.kappa * kappa_mult)
    kst = np.sin(s.kappa * kappa_mult)
    kR = np.array([[kct, kst],
                   [-kst, kct]])

    points = np.array([[0., 0.],
                       np.array([-.2, .2]) * slong])

    points_left = kR.dot(points) + np.array([[-.35 * slat, .3 * slong], [-.35 * slat, .3 * slong]]).transpose()
    points_right = kR.dot(points) + np.array([[.35 * slat, .3 * slong], [.35 * slat, .3 * slong]]).transpose()

    if 'color' in kwargs:
        artist_obj_list.append(plot_in_frame(ax, points_left, R, T, linewidth=2, **kwargs))
        artist_obj_list.append(plot_in_frame(ax, points_right, R, T, linewidth=2, **kwargs))
    else:
        artist_obj_list.append(plot_in_frame(ax, points_left, R, T, color='red', linewidth=2, **kwargs))
        artist_obj_list.append(plot_in_frame(ax, points_right, R, T, color='red', linewidth=2, **kwargs))

    return artist_obj_list


def box_in_frame(ax, cx, cy, w, h, R, T, **kwargs):
    # car outset
    points = np.array([[1, -1, -1, 1, 1], [-1, -1, 1, 1, -1]]).astype(float)

    points[0, :] = points[0, :] * (float(w) / 2.) + cx
    points[1, :] = points[1, :] * (float(h) / 2.) + cy
    artist_obj = plot_in_frame(ax, points, R, T, **kwargs)

    return artist_obj


def plot_in_frame(ax, points, R, T, **kwargs):
    # Apply transformation
    points = R.dot(points)

    artist_obj, = ax.plot(points[0, :] + T[0], points[1, :] + T[1], **kwargs)
    return artist_obj


def plot_path(states, path):
    local_path = np.array(path) #- 1 # compensate for the state offset of 1!
    plt.plot(states[0, local_path], states[1, local_path],
             markersize=5, label='Path', marker='o', linestyle='solid', color='gray')

def animation_init(ax, states, target_state, with_other_vehicle=False, other_vehicle_states=0):
    # Start and goal
    # plot_vehicle_state(ax, vehicle_struct(states, 0), color='blue')

    if with_other_vehicle:
        plot_vehicle_state(ax, vehicle_struct(other_vehicle_states, 0), color='red')

    ax.plot(target_state[0], 2.5, color='green', marker='v', markersize=20)

    # Total path
    plt.plot([0, visual_lim], [4, 4], color='black')
    plt.plot([0, visual_lim], [0, 0], linestyle='dashed', color='gray', linewidth=2.0, dashes=(5, 10))
    plt.plot([0, visual_lim], [-4, -4], color='black')

def animation_update(fig, ax, states, plans, t, terminal_set=0, disc_radius=0., disc_offsets=0, other_vehicle_states=0):
        # Plot the vehicle
        obj = plot_vehicle_state(ax, vehicle_struct(states, int(t)))

        # Visualize collision discs
        if disc_radius > 0.:
            for disc in range(len(disc_offsets)):
                circle = plt.Circle((plans[0, 0, t] + disc_offsets[disc], 0), disc_radius,
                                    color=(0., 0., 0.), alpha=0.3)
                collision_obj = ax.add_patch(circle)
                obj.append(collision_obj)

                circle = plt.Circle((other_vehicle_states[0, 0] + disc_offsets[disc], 0), disc_radius,
                                    color=(0.+0.5, 0., 0.), alpha=0.3)
                collision_obj = ax.add_patch(circle)
                obj.append(collision_obj)

        if terminal_set is not 0:
            new_obj = ax.fill_betweenx([-4, 4], terminal_set.x_lim_b[t, 0], terminal_set.x_lim_b[t, 1], alpha=0.3, color='green')
            obj.append(new_obj)

            for idx in range(2):
                new_obj, = ax.plot([terminal_set.x_lim_b[t, idx], terminal_set.x_lim_b[t, idx]], [-4, 4], color='black')
                obj.append(new_obj)

        # Plot the plan
        for idx in range(len(plans[0, 1:, t])):
            color_scale = idx/((float)(len(plans[0, :, t])))
            circle = plt.Circle((plans[0, idx, t], 0), 0.5, color=(0.1, 0.0, 0.5), alpha=0.8-color_scale*0.5)
            new_obj = ax.add_patch(circle)
            obj.append(new_obj)


        return obj

def make_animation(timesteps, states, plans, target_state, terminal_set=0, with_other_vehicle=False, other_vehicle_states=0, disc_radius=0., disc_offsets=0):

    # Plot the current state
    fig, ax, artist_obj_list = plot_2d()
    ims = []

    for t in range(len(timesteps)):
        ims.append(animation_update(fig, ax, states, plans, t, terminal_set, disc_radius, disc_offsets, other_vehicle_states))

    animation_init(ax, states, target_state, with_other_vehicle, other_vehicle_states)
    anim = animation.ArtistAnimation(fig, ims, repeat=False, interval=250)
    plt.close()

    return anim