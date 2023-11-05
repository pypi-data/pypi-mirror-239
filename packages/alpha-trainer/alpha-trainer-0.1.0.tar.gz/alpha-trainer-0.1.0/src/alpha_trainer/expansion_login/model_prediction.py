import random
from typing import Callable

from ..alpha_classes import AlphaMove, AlphaTrainableGame


def model_prediction(
    state: AlphaTrainableGame,
    model,
    choice_function: Callable[[dict[AlphaMove, float]], AlphaMove] = None,
) -> AlphaTrainableGame:
    if not isinstance(state, AlphaTrainableGame):
        raise ValueError(
            f"State must be an instance of AlphaTrainableGame is {type(state)}"
        )
    probabilities = []
    possible_actions = state.get_possible_actions()
    for action in possible_actions:
        new_state = state.copy().perform(action)
        probability = model.predict_proba([new_state.get_state()])[0, 0] + 1e-12
        probabilities.append(probability)
    if choice_function is None:
        chosen_action = random.choices(possible_actions, probabilities, k=1)[0]
    else:
        chosen_action = choice_function(dict(zip(possible_actions, probabilities)))
    state = state.perform(chosen_action)
    return state
