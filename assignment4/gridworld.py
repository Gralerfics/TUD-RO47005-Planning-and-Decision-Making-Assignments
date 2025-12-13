# Gridworld class with matplotlib
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mdp


# import matplotlib as mpl
# mpl.rcParams['figure.dpi'] = 300


class Gridworld:
    def __init__(
        self,
        size: tuple,
        start_pos: tuple,
        goal_pos: tuple,
        obstacles: list = None,
        low_reward_cells: list = None,
        dpi=50,
        fps=5,
    ):
        self.width = size[0]
        self.height = size[1]
        self.fps = fps
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        self.agent_pos = np.array(start_pos, dtype=int)
        self.start_pos = np.array(start_pos, dtype=int)
        self.goal_pos = np.array(goal_pos, dtype=int)
        self.goal_state = self.position_to_state(self.goal_pos)
        self.start_state = self.position_to_state(self.start_pos)
        self.low_reward_states = (
            [self.position_to_state(pos) for pos in low_reward_cells]
            if low_reward_cells is not None
            else []
        )
        self.dpi = dpi
        # Set obstacles
        if obstacles is not None:
            for obstacle in obstacles:
                self.grid[obstacle[1], obstacle[0]] = 1

        # Set low reward cells
        if low_reward_cells is not None:
            for cell in low_reward_cells:
                self.grid[cell[1], cell[0]] = 2

        # Create trajectory buffer
        self.trajectory = []
        self.trajectory.append(self.agent_pos)

        # Init colors
        self.colors = {
            "empty": (1, 1, 1),
            "obstacle": (0.2, 0.2, 0.2),
            "goal": (0, 1, 0),
            "agent": (0, 0, 1),
            "low_reward": (1, 0, 0),
            "trajectory": (0.5, 0.5, 0.8),
        }

    def state_to_position(self, state):
        return np.unravel_index(state, (self.height, self.width))

    def position_to_state(self, position):
        return np.ravel_multi_index(position, (self.height, self.width))

    def get_trajectory_from_state_sequence(self, state_sequence):
        return [self.state_to_position(state) for state in state_sequence]

    def _draw_grid(self):
        # Draw grid with black border between cells
        for y in range(self.height):
            for x in range(self.width):
                # Draw cell with color depending on cell type
                color = self.colors["empty"]
                if self.grid[y, x] == 1:
                    color = self.colors["obstacle"]
                elif self.grid[y, x] == 2:
                    color = self.colors["low_reward"]
                elif (x, y) == tuple(self.goal_pos):
                    color = self.colors["goal"]
                self.ax.add_patch(
                    plt.Rectangle((x, y), 1, 1, color=color, fill=True, zorder=0)
                )
                self.ax.add_patch(
                    plt.Rectangle(
                        (x, y), 1, 1, color="black", fill=False, linewidth=1, zorder=1
                    )
                )

    def _create_figure(self):
        # Create figure with size (width * scale, height * scale)
        self.fig = plt.figure(figsize=(self.width, self.height), dpi=self.dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_aspect("equal")
        self.ax.set_facecolor("white")

    def _draw_agent(self):
        x = self.agent_pos[0]
        y = self.agent_pos[1]
        # Draw agent as blue circle in center of cell
        self.ax.add_patch(
            plt.Circle(
                (x + 0.5, y + 0.5), 0.4, color=self.colors["agent"], fill=True, zorder=5
            )
        )

    def _draw_trajectory(self, i=None):
        # Draw trajectory as red line
        if i is None:
            trajectory = np.array(self.trajectory)
        else:
            trajectory = np.array(self.trajectory[: i + 1])
        self.ax.plot(
            trajectory[:, 0] + 0.5,
            trajectory[:, 1] + 0.5,
            color=self.colors["trajectory"],
            linewidth=5,
            zorder=5,
        )

    def _draw_history(self, i):
        self.ax.clear()
        self.agent_pos = self.trajectory[i]
        self._draw_grid()
        self._draw_trajectory(i)
        self._draw_agent()
        return self.ax

    def set_agent_pos(self, x, y):
        self.agent_pos = np.array([x, y])
        # Add new position to trajectory
        self.trajectory.append(self.agent_pos)

    def show(self):
        self._create_figure()
        self._draw_grid()
        self._draw_trajectory()
        self._draw_agent()
        plt.show()

    def validate_trajectory(self, trajectory):
        # iterate over all positions transitions and check that they are all "dynamically feasible"
        for i in range(len(self.trajectory) - 1):
            position = np.array(self.trajectory[i])
            next_position = np.array(self.trajectory[i + 1])
            delta_p = next_position - position
            # we cannot step more than one cell in any direction
            assert np.all(np.abs(delta_p) <= 1)
            # we cannot step into obstacles
            assert self.grid[next_position[1], next_position[0]] != 1

    def animate(self, trajectory=None):
        if trajectory is not None:
            self.trajectory = trajectory

        self.validate_trajectory(trajectory)

        self._create_figure()

        anim = animation.FuncAnimation(
            self.fig,
            self._draw_history,
            frames=len(self.trajectory),
            interval=1000 / self.fps,
        )
        plt.show()
        return anim

    def draw_policy(self, policy, on_value_function = False):
        if on_value_function:
            self.draw_value_function(policy)
        else:
            self._create_figure()
            self._draw_grid()
        # Draw policy as arrows inside each cell in direction of action
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y, x] == 1 or (x, y) == tuple(self.goal_pos):
                    continue
                state = self.position_to_state((x, y))
                action = policy(state)
                if action == 2:
                    dx = 0
                    dy = 0.3
                elif action == 3:
                    dx = 0
                    dy = -0.3
                elif action == 1:
                    dx = -0.3
                    dy = 0
                else:
                    dx = 0.3
                    dy = 0
                self.ax.arrow(
                    x + 0.5,
                    y + 0.5,
                    dx,
                    dy,
                    head_width=0.15,
                    head_length=0.15,
                    color=self.colors["agent"],
                    zorder=10,
                )
                self.ax.add_patch(
                    plt.Circle(
                        (x + 0.5, y + 0.5), 0.05, color=self.colors["agent"], fill=True, zorder=5
                    )
                )

    def draw_value_function(self, policy):
        self._create_figure()
        # Draw grid with color map depending on value function
        self._draw_grid()
        value_function = np.zeros((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                state = self.position_to_state((x, y))
                value_function[y, x] = policy.get_value(state)
        colormap = self.ax.imshow(
            value_function,
            cmap="viridis",
            interpolation="nearest",
            extent=[0, self.width, 0, self.height],
            origin="lower",
            zorder=0,
            vmin=np.min(value_function),
            vmax=np.max(value_function),
        )
        for y in range(self.height):
            for x in range(self.width):
                # Draw obstacle cells as black
                if self.grid[y, x] == 1:
                    self.ax.add_patch(
                        plt.Rectangle(
                            (x, y), 1, 1, color="black", fill=True, zorder=1
                        )
                    )
        self.fig.colorbar(colormap)

    def move_if_feasible(self, start_position, step):
        px, py = start_position
        new_x, new_y = px + step[0], py + step[1]

        # Check if new position is inside grid
        if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
            # Stay in same position
            new_x = px
            new_y = py

        # Check if new position is obstacle
        if self.grid[new_y, new_x] == 1:
            # Stay in same position
            new_x = px
            new_y = py

        return (new_x, new_y)

    def derive_mdp(
        self,
        goal_reward: int = 100,
        transition_noise: float = 0.01,
        discount_factor: float = 0.99,
        low_reward_penalty: float = -100,
    ):
        number_of_states = self.width * self.height
        number_of_actions = 4
        transition_table = np.zeros(
            (number_of_states, number_of_actions, number_of_states)
        )
        states = np.arange(number_of_states)
        positions = [self.state_to_position(state) for state in states]
        actions = np.arange(number_of_actions)
        action_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for state, position in zip(states, positions):
            for action, step in zip(actions, action_offsets):
                # Calculate new position
                nominal_next_position = self.move_if_feasible(position, step)
                # compute noisy step candidates in laterla direction
                if step[0] == 0:
                    noisy_steps = [(-1, 0), (1, 0)]
                else:
                    noisy_steps = [(0, -1), (0, 1)]

                noisy_next_positions = [
                    self.move_if_feasible(position, step) for step in noisy_steps
                ]

                # Add the nominal transition
                transition_table[
                    state, action, self.position_to_state(nominal_next_position)
                ] = (1 - transition_noise)
                # add the noisy transitions
                for noisy_next_position in noisy_next_positions:
                    transition_table[
                        state, action, self.position_to_state(noisy_next_position)
                    ] += transition_noise / len(noisy_next_positions)

        # at the goal state, we can only stay
        transition_table[self.goal_state, :, :] = 0
        transition_table[self.goal_state, :, self.goal_state] = 1

        # if we are in a low reward state, we can only stay
        transition_table[self.low_reward_states, :, :] = 0
        transition_table[self.low_reward_states, :, self.low_reward_states] = 1

        reward_table = np.zeros((number_of_states, number_of_actions, number_of_states))
        # for all non-goal states, we get a step penalty of 1
        reward_table[:, :, :] = -1
        # if we transition into the goal we get a higher reward, after that we can no longer get a reward
        reward_table[:, :, self.goal_state] = goal_reward
        reward_table[self.goal_state, :, :] = 0
        # if we transition into a low reward state weg et a lower reward, after that we can no longer get a reward
        reward_table[:, :, self.low_reward_states] = low_reward_penalty
        reward_table[self.low_reward_states, :, :] = 0

        return mdp.MarkovDecisionProcess(
            transition_table, reward_table, discount_factor
        )

    @staticmethod
    def setup_simple_world():
        world = Gridworld(
            size=(3, 3),
            start_pos=(0, 2),
            goal_pos=(2, 2),
            obstacles=[(1, 2)],
            low_reward_cells=[(1, 1)],
        )
        return world

    @staticmethod
    def setup_medium_world():
        world = Gridworld(
            size=(9, 9),
            start_pos=(0, 5),
            goal_pos=(8, 5),
            # obstacles=[(1, 2), (1, 1)],
            low_reward_cells=[
                (3, 3),
                (3, 4),
                (3, 5),
                (4, 3),
                (4, 4),
                (4, 5),
                (5, 3),
                (5, 4),
                (5, 5),
            ],
        )
        return world

    @staticmethod
    def setup_large_world():
        world = Gridworld(
            size=(20, 20),
            start_pos=(0, 5),
            goal_pos=(19, 5),
            # obstacles=[(1, 2), (1, 1)],
            low_reward_cells=[
                (3, 3),
                (3, 4),
                (3, 5),
                (4, 3),
                (4, 4),
                (4, 5),
                (5, 3),
                (5, 4),
                (5, 5),
                (6, 3),
                (6, 4),
                (6, 5),
                (7, 3),
                (7, 4),
                (7, 5),
                (8, 3),
                (8, 4),
                (8, 5),
                (9, 3),
                (9, 4),
                (9, 5),
            ],
        )
        return world


if __name__ == "__main__":
    agent_pos = (0, 2)
    # Create gridworld
    obj = Gridworld(
        (5, 5),
        (0, 2),
        (4, 1),
        [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    )
    # move agent up
    obj.set_agent_pos(0, 3)
    obj.set_agent_pos(0, 4)
    obj.set_agent_pos(1, 4)

    obj.animate()
