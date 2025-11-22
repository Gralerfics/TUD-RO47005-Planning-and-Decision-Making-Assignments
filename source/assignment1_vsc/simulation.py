import numpy as np
import visualization
from tqdm.notebook import tqdm

def simulate(vehicle, dt, T, x_init, x_target, plan_length, control_func, plot_trajectories=True):
    # Initialise the output arrays
    x_real = np.zeros((2, T+1))
    x_all = np.zeros((2, plan_length+1, T+1))
    u_real = np.zeros((1, T))
    x_real[:, 0] = x_init
    theta_all = np.zeros((T))
    timesteps = np.linspace(0, dt, T)

    for t in tqdm(range(0, T), 'Simulating'):
        # Compute the control input (and apply it)
        u_out, x_out, x_all_out, theta_out = control_func(x_real[:, t]) #vehicle, x_real[:, t], x_target)

        # Next x is the x in the second state
        x_real[:, t+1] = x_out
        x_all[:, :, t] = x_all_out # Save the plan (for visualization)

        # Used input is the first input
        u_real[:, t] = u_out

        theta_all[t] = theta_out
        # print("Input: " + str(u_out))

    # Function that plots the trajectories.
    # The plot is stored with the name of the first parameter
    if plot_trajectories:
        visualization.plot_trajectories('mpc_control.eps', x_real, u_real, T)

    return x_real, u_real, x_all, timesteps, theta_all