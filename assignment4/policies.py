import numpy as np
import numpy.typing as nptyping


class QValuePolicy:
    def __init__(self, qvalue_table: nptyping.NDArray):
        self.qvalue_table = qvalue_table

    def __call__(self, state: int) -> np.intp:
        # return the action with the highest q-value
        return np.argmax(self.qvalue_table[state])

    def get_value(self, state: int) -> float:
        # return the value of the state
        return np.max(self.qvalue_table[state])

    def _get_all_best_actions(self, state=None, atol=0):
        def get_best_actions_for_single_state(state):
            return np.flatnonzero(
                np.isclose(
                    self.qvalue_table[state],
                    np.max(self.qvalue_table[state]),
                    atol=atol,
                )
            )

        if state is None:
            return [
                get_best_actions_for_single_state(state)
                for state in range(self.qvalue_table.shape[0])
            ]

        return get_best_actions_for_single_state(state)

class OnlinePolicy:
    def __init__(self, get_action_and_utiltiy):
        self.get_action_and_utiltiy = get_action_and_utiltiy

    def __call__(self, state):
        return self.get_action_and_utiltiy(state)[0]

    def get_value(self, state):
        return self.get_action_and_utiltiy(state)[1]

class EpsilonGreedyPolicy:
    def __init__(self, inner_policy, epsilon):
        self.inner_policy = inner_policy
        self.epsilon = epsilon

    def __call__(self, state):
        if np.random.uniform() < self.epsilon:
            # explore
            random_action = np.random.choice(self.inner_policy.qvalue_table.shape[1])
            return random_action
        # follow the action recommended by the inner policy
        return self.inner_policy(state)
