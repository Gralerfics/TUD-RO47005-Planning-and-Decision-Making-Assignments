import numpy as np
import numpy.typing as nptyping
from typing import Union, Tuple


class MarkovDecisionProcess:
    def __init__(
        self,
        transition_table: np.ndarray,
        reward_table: np.ndarray,
        discount_factor: float = 1,
    ):
        # sanity checking the transition_table: for all state-action pairs, the sum of transition probabilities must be 1
        for state in range(transition_table.shape[0]):
            for action in range(transition_table.shape[1]):
                assert np.isclose(
                    np.sum(transition_table[state, action, :]), 1
                ), f"transition probabilities for state {state} and action {action} do not sum to 1"

        self.transition_table = transition_table
        self.reward_table = reward_table
        self.discount_factor = discount_factor

    def transition(
        self, state: int, action: int, next_state: Union[int, None] = None
    ) -> np.ndarray:
        transition_probabilities = self.transition_table[state, action]
        # if no next state is provided, return transition probabilities for all next states
        if next_state is None:
            return transition_probabilities
        return transition_probabilities[next_state]

    def reward(
        self, state: int, action: int, next_state: Union[int, None] = None
    ) -> float:
        rewards = self.reward_table[state, action]
        # if no next state is provided, return the expected reward for all next states
        if next_state is None:
            transition_probabilities = self.transition(state, action)
            weighted_rewards = transition_probabilities * rewards
            return sum(weighted_rewards)
        return rewards[next_state]

    def sample_transition(self, state: int, action: int) -> Tuple[int, float]:
        next_state = np.random.choice(
            self.transition_table.shape[2], p=self.transition(state, action)
        )
        reward = self.reward(state, action, next_state)
        return next_state, reward

    @property
    def num_states(self) -> int:
        return self.transition_table.shape[0]

    @property
    def num_actions(self) -> int:
        return self.transition_table.shape[1]

    def simulate(self, agent, number_of_steps, initial_state):
        state = initial_state
        states = []
        actions = []
        rewards = []

        for _ in range(number_of_steps):
            states.append(state)
            policy = agent.get_policy()
            action = policy(state)
            next_state, reward = self.sample_transition(state, action)
            actions.append(action)
            rewards.append(reward)
            agent.update_model(state, action, next_state, reward)
            state = next_state

        return states, actions, rewards
