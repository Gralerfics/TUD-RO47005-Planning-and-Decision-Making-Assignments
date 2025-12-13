import gridworld
import numpy as np
from tqdm import tqdm


def test_qvalue_iteration_planner(agent_constructor, world=None, ground_truth=None):
    # setup a simple test mdp
    if not world:
        world = gridworld.Gridworld.setup_simple_world()
        ground_truth = get_simple_ground_truth()
    assert ground_truth is not None
    ground_truth_optimal_actions, ground_truth_qvalues = ground_truth
    problem = world.derive_mdp()

    # setup the planner
    agent = agent_constructor(problem=problem)
    # check the policy computed by the student
    policy = agent.get_policy()

    for state in range(problem.num_states):
        # skip states that are not reachable (i.e. obstacles)
        position = world.state_to_position(state)
        if world.grid[position[1], position[0]] != 0:
            continue
        assert (
            policy(state) in ground_truth_optimal_actions[state]
        ), "Your policy computes a suboptimal action for state {}.".format(state)

    # go over all the state-action pairs and check that the qvalues are correct
    for state in range(problem.num_states):
        # skip states that are not reachable (i.e. obstacles)
        position = world.state_to_position(state)
        if world.grid[position[1], position[0]] != 0:
            continue
            continue
        for action in range(problem.num_actions):
            assert np.isclose(
                policy.qvalue_table[state, action],
                ground_truth_qvalues[state, action],
                rtol=1e-3,
            ), "Your solution produces the wrong qvalue for state {} and action {}".format(
                state, action
            )

    print("--- Your solution passed all the tests! ---")


def test_forward_search_planner(agent_constructor, world=None, ground_truth=None):
    # setup a simple test mdp
    if not world:
        world = gridworld.Gridworld.setup_simple_world()
        ground_truth = get_simple_ground_truth()
    assert ground_truth is not None
    ground_truth_optimal_actions, ground_truth_qvalues = ground_truth
    problem = world.derive_mdp()

    def utility_function_estimate(state):
        return np.max(ground_truth_qvalues[state])

    # setup the planner
    agent = agent_constructor(
        problem=problem, horizon=2, utility_function_estimate=utility_function_estimate
    )
    # check the policy computed by the student
    policy = agent.get_policy()

    for state in range(problem.num_states):
        # skip states that are not reachable (i.e. obstacles)
        position = world.state_to_position(state)
        if world.grid[position[1], position[0]] != 0:
            continue
        assert (
            policy(state) in ground_truth_optimal_actions[state]
        ), "Your policy computes a suboptimal action for state {}.".format(state)

    for state in range(problem.num_states):
        # skip states that are not reachable (i.e. obstacles)
        position = world.state_to_position(state)
        if world.grid[position[1], position[0]] != 0:
            continue
        u = agent.forward_search(state, agent.horizon)[1]
        ustar = utility_function_estimate(state)
        assert np.isclose(
            u, ustar, rtol=1e-3
        ), "Your solution produces the wrong state value for state {}. Computed value is {}, but the correct value is {}.".format(
            state, u, ustar
        )

    print("--- Your solution passed all the tests! ---")


def test_qlearning(
    agent_constructor,
    world=None,
    ground_truth=None,
    number_of_episodes=10000,
    number_of_steps_per_episode=20,
    initial_state=2,
):

    # setup a simple test mdp
    if not world:
        world = gridworld.Gridworld.setup_simple_world()
        ground_truth = get_simple_ground_truth()
    assert ground_truth is not None
    ground_truth_optimal_actions, ground_truth_qvalues = ground_truth
    problem = world.derive_mdp()

    # setup the planner
    agent = agent_constructor(
        num_states=problem.num_states,
        num_actions=problem.num_actions,
        discount_factor=problem.discount_factor,
    )
    # first, we have to train the policy for a while to get a good estimate of the qvalues.
    progressbar = tqdm(range(number_of_episodes))
    progressbar.set_description("Training")
    for _ in progressbar:
        # initial_state = np.random.randint(num_states)
        problem.simulate(agent, number_of_steps_per_episode, initial_state)

    # disable exploration for testing
    policy = agent.get_policy().inner_policy
    print("Goal state", world.goal_state)
    for state in range(problem.num_states):
        # skip states that are not reachable (i.e. obstacles)
        position = world.state_to_position(state)
        if world.grid[position[1], position[0]] != 0:
            continue
        assert (
            policy(state) in ground_truth_optimal_actions[state]
        ), "Your policy computes a suboptimal action for state {}.".format(state)

    # go over all the state-action pairs and check that the qvalues are correct
    for state in range(problem.num_states):
        # skip states that are not reachable (i.e. obstacles)
        position = world.state_to_position(state)
        if world.grid[position[1], position[0]] != 0:
            continue
        for action in range(problem.num_actions):
            assert np.isclose(
                policy.qvalue_table[state, action],
                ground_truth_qvalues[state, action],
                rtol=1e-1,
            ), "Your solution produces the wrong qvalue for state {} and action {}. \
                You computed {} but the correct value is {}.".format(
                state,
                action,
                policy.qvalue_table[state, action],
                ground_truth_qvalues[state, action],
            )

    print("--- Your solution passed all the tests! ---")


def visualize_qlearning(
    agent_constructor,
    world,
    number_of_steps_per_episode=20,
    number_of_episodes=30000,
    initial_state=2,
    epsilon=0.5,
    show_animation=False,
):
    problem = world.derive_mdp()

    # setup a q-learning agent
    agent = agent_constructor(
        num_states=problem.num_states,
        num_actions=problem.num_actions,
        discount_factor=problem.discount_factor,
        epsilon=epsilon,
    )

    # train the agent for a few episodes to get some experience
    progressbar = tqdm(range(number_of_episodes))
    progressbar.set_description("Training")
    for _ in progressbar:
        # initial_state = np.random.randint(num_states)
        problem.simulate(agent, number_of_steps_per_episode, initial_state)

    # visualize the policy and value function
    policy = agent.get_policy().inner_policy
    world.draw_policy(policy, on_value_function=True)

    # disable exploration for the final visualization
    if show_animation:
        agent.set_epsilon(0)
        states, *_ = problem.simulate(
            agent, number_of_steps=20, initial_state=initial_state
        )
        trajectory = world.get_trajectory_from_state_sequence(states)
        animation = world.animate(trajectory)
        return animation


def get_simple_ground_truth():

    optimal_actions, qvalue_table = (
        [
            np.array([0]),
            np.array([3]),
            np.array([3]),
            np.array([0]),
            np.array([0, 1, 2, 3]),
            np.array([0]),
            np.array([2]),
            np.array([2]),
            np.array([0, 1, 2, 3]),
        ],
        np.array(
            [
                [92.02739381, 90.09283835, 87.28921028, 90.11689005],
                [-98.12266643, 87.25570217, 84.44225289, 89.14230276],
                [85.36905086, 85.36905086, 85.35959445, 87.23196455],
                [94.00122827, 89.16635445, -98.07451025, 92.06609358],
                [0.0, 0.0, 0.0, 0.0],
                [98.98497563, 84.49097413, 96.95197259, -98.07320203],
                [95.00085197, 92.10053361, 96.96043485, 94.97618243],
                [97.00012877, -98.02504585, 98.98497563, 94.02589782],
                [0.0, 0.0, 0.0, 0.0],
            ]
        ),
    )

    return optimal_actions, qvalue_table
